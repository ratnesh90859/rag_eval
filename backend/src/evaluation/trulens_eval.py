import os
from trulens.core import TruSession, Metric
from trulens.apps.llamaindex import TruLlama
from trulens.providers.litellm import LiteLLM
from src.core.config import settings

# Initialize Session
session = TruSession()
os.environ["GEMINI_API_KEY"] = settings.google_api_key
gemini_provider = LiteLLM(model_engine="gemini/gemini-2.5-flash")

# Define Metrics for TruLlama wrapper
m_answer_relevance = Metric(implementation=gemini_provider.relevance_with_cot_reasons, name="Answer Relevance").on_input_output()
m_context_relevance = Metric(implementation=gemini_provider.context_relevance_with_cot_reasons, name="Context Relevance").on_prompt().on_context(collect_list=True)
m_groundedness = Metric(implementation=gemini_provider.groundedness_measure_with_cot_reasons, name="Groundedness").on_context(collect_list=True).on_response()
metrics = [m_answer_relevance, m_context_relevance, m_groundedness]

def get_trulens_recorder(query_engine):
    return TruLlama(query_engine, app_name="Enterprise RAG App", feedbacks=metrics)

import concurrent.futures

def evaluate_realtime(query: str, contexts: list[str], response: str):
    """
    Evaluates a single interaction synchronously so we can return the scores immediately to the UI.
    Optimized to run all three checks concurrently via ThreadPoolExecutor.
    """
    # Join contexts into a single string
    context_str = "\n\n".join(contexts)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # Submit the three evaluation tasks to run in parallel
        future_c = executor.submit(gemini_provider.context_relevance_with_cot_reasons, query, context_str)
        future_g = executor.submit(gemini_provider.groundedness_measure_with_cot_reasons, context_str, response)
        future_a = executor.submit(gemini_provider.relevance_with_cot_reasons, query, response)
        
        # Wait for results
        c_score, c_reason = future_c.result()
        g_score, g_reason = future_g.result()
        a_score, a_reason = future_a.result()
    
    return {
        "context_relevance": c_score,
        "context_reason": c_reason,
        "groundedness": g_score,
        "groundedness_reason": g_reason,
        "answer_relevance": a_score,
        "answer_reason": a_reason
    }
