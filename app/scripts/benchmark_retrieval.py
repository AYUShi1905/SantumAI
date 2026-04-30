import sys
import os
import time
import asyncio

# Add the app directory to sys.path
sys.path.append(os.path.join(os.getcwd()))

from core.config import settings
from langchain_community.embeddings import JinaEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.http import models as rest

def benchmark():
    print(f"--- Starting Benchmark ---")
    print(f"Targeting Model: {settings.JINA_EMBEDDING_MODEL}")
    print(f"Targeting Collection: {settings.COLLECTION_NAME}")
    
    # 1. Test Jina AI Latency
    print("\n[1/2] Testing Jina AI Embedding Latency...")
    embeddings = JinaEmbeddings(
        jina_api_key=settings.JINA_API_KEY,
        model_name=settings.JINA_EMBEDDING_MODEL
    )
    
    test_query = "What are the common psychological impacts of childhood trauma?"
    
    start_time = time.time()
    query_vector = embeddings.embed_query(test_query)
    jina_duration = time.time() - start_time
    
    print(f"✅ Jina Embedding completed in: {jina_duration:.4f} seconds")
    print(f"Vector Dimensions: {len(query_vector)}")

    # 2. Test Qdrant Latency
    print("\n[2/2] Testing Qdrant Search Latency...")
    client = QdrantClient(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY
    )
    
    start_time = time.time()
    search_result = client.search(
        collection_name=settings.COLLECTION_NAME,
        query_vector=query_vector,
        limit=5
    )
    qdrant_duration = time.time() - start_time
    
    print(f"✅ Qdrant Search completed in: {qdrant_duration:.4f} seconds")
    print(f"Results Found: {len(search_result)}")

    print("\n--- Final Results ---")
    print(f"Jina AI (Embeddings): {jina_duration:.2f}s ({(jina_duration/(jina_duration+qdrant_duration)*100):.1f}%)")
    print(f"Qdrant (Search):     {qdrant_duration:.2f}s ({(qdrant_duration/(jina_duration+qdrant_duration)*100):.1f}%)")
    print(f"Total Retrieval Time: {(jina_duration + qdrant_duration):.2f}s")

if __name__ == "__main__":
    benchmark()
