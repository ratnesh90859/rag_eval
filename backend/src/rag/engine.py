import chromadb
from llama_index.core import VectorStoreIndex, Settings
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.storage.storage_context import StorageContext
from llama_index.core.postprocessor import MetadataReplacementPostProcessor
from src.core.config import settings

def init_settings():
    Settings.llm = GoogleGenAI(model="gemini-2.5-flash", api_key=settings.google_api_key, temperature=0.1)
    Settings.embed_model = GoogleGenAIEmbedding(model_name="gemini-embedding-001", api_key=settings.google_api_key)
    Settings.chunk_size = 256
    Settings.chunk_overlap = 50

def get_query_engine():
    init_settings()
    
    db = chromadb.PersistentClient(path=settings.chroma_db_dir)
    chroma_collection = db.get_or_create_collection("rag_collection")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        storage_context=storage_context,
    )
    
    return index.as_query_engine(
        similarity_top_k=5,
        node_postprocessors=[
            MetadataReplacementPostProcessor(target_metadata_key="window")
        ]
    )

def retrieve_nodes(query: str):
    engine = get_query_engine()
    # Execute retrieval to get nodes without synthesizing
    retriever = engine.retriever
    nodes = retriever.retrieve(query)
    # Apply postprocessors to get the expanded window text
    for postprocessor in engine._node_postprocessors:
        nodes = postprocessor.postprocess_nodes(nodes, query_bundle=engine._get_prompt_modules().get('query_bundle', query))
    return nodes
