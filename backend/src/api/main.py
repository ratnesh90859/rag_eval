import os
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
from typing import Optional
from src.rag.engine import get_query_engine
from src.evaluation.trulens_eval import get_trulens_recorder, evaluate_realtime

app = FastAPI(title="Enterprise RAG Evaluation API")

# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str

import time

class ChatResponse(BaseModel):
    query_id: str
    query: str
    answer: str
    contexts: list[str]
    latency_seconds: float

# Global in-memory store for evaluation results
eval_results_store = {}

# Initialize Engine globally
engine = get_query_engine()
recorder = get_trulens_recorder(engine)

def run_evaluation_task(query_id: str, query: str, contexts: list[str], answer: str):
    eval_scores = evaluate_realtime(query, contexts, answer)
    eval_results_store[query_id] = eval_scores

@app.post("/api/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest, background_tasks: BackgroundTasks):
    start_time = time.time()
    query_id = str(uuid.uuid4())
    try:
        # 1. Run the RAG Query (wrapped in TruLens so it logs to DB)
        with recorder as recording:
            response = engine.query(request.query)
        
        # Extract the exact retrieved text chunks
        contexts = [node.get_content() for node in response.source_nodes]
        answer = response.response
        
        # 2. Trigger evaluation in the background
        background_tasks.add_task(run_evaluation_task, query_id, request.query, contexts, answer)
        
        latency = time.time() - start_time
        
        return ChatResponse(
            query_id=query_id,
            query=request.query,
            answer=answer,
            contexts=contexts,
            latency_seconds=round(latency, 2)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/eval/{query_id}")
def get_evaluation(query_id: str):
    if query_id in eval_results_store:
        return {"status": "completed", "evaluation": eval_results_store[query_id]}
    return {"status": "pending"}
