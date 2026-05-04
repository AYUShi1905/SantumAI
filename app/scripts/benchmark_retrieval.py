import sys
import os
import time
import asyncio

# Add the app directory to sys.path
sys.path.append(os.path.join(os.getcwd()))

from core.config import settings
from langchain_community.embeddings import JinaEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.http import models as rest

def benchmark():
    print(f"--- Embedding Comparison Benchmark ---")
    
    test_query = "What are the common psychological impacts of childhood trauma?"
    
    # 1. Test Jina AI Latency (If key exists)
    jina_duration = None
    if settings.JINA_API_KEY:
        print("\n[1/3] Testing Jina AI Embedding Latency...")
        try:
            jina_embeddings = JinaEmbeddings(
                jina_api_key=settings.JINA_API_KEY,
                model_name=settings.JINA_EMBEDDING_MODEL
            )
            start_time = time.time()
            jina_embeddings.embed_query(test_query)
            jina_duration = time.time() - start_time
            print(f"✅ Jina Embedding completed in: {jina_duration:.4f} seconds")
        except Exception as e:
            print(f"❌ Jina test failed: {e}")
    else:
        print("\n[1/3] Skipping Jina (No API Key)")

    # 2. Test Gemini AI Latency
    print("\n[2/3] Testing Google Gemini Embedding Latency...")
    gemini_duration = None
    try:
        gemini_embeddings = GoogleGenerativeAIEmbeddings(
            google_api_key=settings.GOOGLE_API_KEY,
            model=settings.GOOGLE_EMBEDDING_MODEL,
            task_type="retrieval_query",
            output_dimensionality=768
        )
        start_time = time.time()
        vector = gemini_embeddings.embed_query(test_query)
        gemini_duration = time.time() - start_time
        print(f"✅ Gemini Embedding completed in: {gemini_duration:.4f} seconds")
        print(f"Vector Dimensions: {len(vector)}")
    except Exception as e:
        print(f"❌ Gemini test failed: {e}")

    # 3. Test Qdrant Search Latency
    print("\n[3/3] Testing Qdrant Search Latency...")
    client = QdrantClient(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY
    )
    
    qdrant_duration = None
    if gemini_duration:
        try:
            # We use gemini vector for search test
            vector = gemini_embeddings.embed_query(test_query)
            start_time = time.time()
            client.query_points(
                collection_name=settings.COLLECTION_NAME,
                query=vector,
                limit=5
            )
            qdrant_duration = time.time() - start_time
            print(f"✅ Qdrant Search (query_points) completed in: {qdrant_duration:.4f} seconds")
        except Exception as e:
            print(f"❌ Qdrant search test failed: {e}")

    print("\n--- Final Results ---")
    if jina_duration:
        print(f"Jina AI Latency:   {jina_duration:.2f}s")
    if gemini_duration:
        print(f"Gemini AI Latency: {gemini_duration:.2f}s")
    if qdrant_duration:
        print(f"Qdrant Search:     {qdrant_duration:.2f}s")


if __name__ == "__main__":
    benchmark()
