# Implementation Plan: RAG Data Embedding & Qdrant Upsert

This document outlines the step-by-step plan to generate vector embeddings for the new RAG dataset and upload (upsert) them into the Qdrant vector database.

---

## 1. Prerequisites & Environment

The script will read configurations from `app/core/config.py` and the local `.env` file:
* **Embedding Model**: `gemini-embedding-001` (via Google Gemini API).
* **Vector DB**: Qdrant Cloud (via `QDRANT_URL` and `QDRANT_API_KEY`).
* **Source Folder**: [00_Docs/RAG_Data/01_Embed_Ready](file:///home/ubuntu/Ayushi/SantumAI/00_Docs/RAG_Data/01_Embed_Ready) (contains the 11 JSON files).

> [!IMPORTANT]
> **Gemini Free-Tier Rate Limits**: To prevent HTTP `429 Too Many Requests` errors from the Gemini Embeddings API, the script **must** adhere to the rate-limiting settings defined in `Settings`:
> * `EMBEDDING_BATCH_SIZE = 5`
> * `EMBEDDING_DELAY_SECONDS = 10.0`

---

## 2. Metadata Pruning Strategy

To optimize database search speeds and payload size, we will discard redundant fields during the import process. 

### Fields to Keep:
* `id` (string)
* `chunk_type` (string - essential for tier restrictions)
* `domain` (string)
* `topic` (string)
* `source_file` (string)
* `source_family` (string)
* `risk_level` (string)
* `content` (string - the text context for the LLM)

### Fields to Discard:
* `embedding_text` (redundant with `content`)
* `example_queries` (unused at runtime)
* `llm_orchestration`, `governance`, `response_style`, `response_constraints` (unused LLM configs)

---

## 3. Step-by-Step Upload Flow

1. **Clear Existing Qdrant Collection**: Since we are discarding all old data and replacing it with the new client dataset, we should delete and recreate the `Santum_AI` collection to ensure a clean slate.
2. **Read Source JSON Files**: Scan and read all 11 JSON files from the `01_Embed_Ready` folder.
3. **Parse and Prune**: Loop through all chunks, extracting the `content` and building the pruned metadata dictionary.
4. **Batch Embedding Generation**:
   * Send the `content` strings to the Google Gemini Embedding API in batches of 5.
   * Sleep for 10 seconds between batches to stay within rate limits.
5. **Upsert into Qdrant**: Upload the generated vectors along with the pruned metadata to Qdrant.

---

## 4. Pseudo-Code Script Outline (`scripts/embed_rag_data.py`)

Here is the conceptual structure for the upload script:

```python
import os
import json
import time
import glob
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from google.generativeai import embed_content
from app.core.config import settings

def run_embedding_pipeline():
    # 1. Initialize Clients
    qdrant = QdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY)
    
    # 2. Reset Qdrant Collection
    qdrant.recreate_collection(
        collection_name=settings.COLLECTION_NAME,
        vectors_config=VectorParams(size=768, distance=Distance.COSINE) # Gemini embeds are 768 dimensions
    )
    
    # 3. Read All JSON Files
    json_files = glob.glob("00_Docs/RAG_Data/01_Embed_Ready/*.json")
    
    all_chunks = []
    for filepath in json_files:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            all_chunks.extend(data)
            
    print(f"Loaded {len(all_chunks)} chunks for embedding.")
    
    # 4. Batch and Upload
    batch_size = settings.EMBEDDING_BATCH_SIZE
    delay = settings.EMBEDDING_DELAY_SECONDS
    
    for i in range(0, len(all_chunks), batch_size):
        batch = all_chunks[i:i + batch_size]
        texts = [item["content"] for item in batch]
        
        # Call Gemini Embedding API
        response = embed_content(
            model=f"models/{settings.GOOGLE_EMBEDDING_MODEL}",
            content=texts,
            task_type="retrieval_document"
        )
        embeddings = response["embedding"]
        
        # Prepare Points for Qdrant
        points = []
        for idx, item in enumerate(batch):
            # Prune metadata
            metadata = {
                "id": item["id"],
                "chunk_type": item.get("chunk_type", "N/A"),
                "domain": item.get("domain", "N/A"),
                "topic": item.get("topic", "N/A"),
                "source_file": item.get("source_file", "N/A"),
                "source_family": item.get("source_family", "N/A"),
                "risk_level": item.get("risk_level", "low"),
                "content": item["content"] # Saved as metadata payload for retrieval
            }
            
            points.append(PointStruct(
                id=hash(item["id"]) % (10**10), # Numeric ID format for Qdrant
                vector=embeddings[idx],
                payload=metadata
            ))
            
        # Upsert Batch
        qdrant.upsert(collection_name=settings.COLLECTION_NAME, points=points)
        print(f"Uploaded batch {i // batch_size + 1} / {len(all_chunks) // batch_size + 1}")
        
        # Rate Limit Sleep
        time.sleep(delay)

    print("Embedding pipeline completed successfully!")
```

---
*Created: July 1, 2026*
