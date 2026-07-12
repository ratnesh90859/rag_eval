import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import chromadb
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.node_parser import SentenceWindowNodeParser
from src.core.config import settings
from src.rag.engine import init_settings

def run_ingestion():
    init_settings()
    
    print(f"Loading documents from {settings.data_dir}...")
    documents = SimpleDirectoryReader(input_dir=settings.data_dir).load_data()
    print(f"Loaded {len(documents)} documents.")

    print("Parsing documents into sentence windows...")
    node_parser = SentenceWindowNodeParser.from_defaults(
        window_size=3,
        window_metadata_key="window",
        original_text_metadata_key="original-text"
    )
    nodes = node_parser.get_nodes_from_documents(documents)
    
    print(f"Created {len(nodes)} nodes. Connecting to ChromaDB at {settings.chroma_db_dir}...")
    db = chromadb.PersistentClient(path=settings.chroma_db_dir)
    chroma_collection = db.get_or_create_collection("rag_collection")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    print("Indexing nodes into ChromaDB...")
    VectorStoreIndex(
        nodes,
        storage_context=storage_context,
        show_progress=True
    )
    print("Ingestion complete!")

if __name__ == "__main__":
    run_ingestion()
