# Implementation Plan: RAG Data Embedding & Qdrant Upsert

This document outlines the step-by-step plan to generate vector embeddings for the new RAG dataset and upload (upsert) them into the Qdrant vector database.

---

## 1. Prerequisites & Environment

The script will read configurations from `app/core/config.py` and the local `.env` file:
* **Embedding Model**: `text-embedding-3-small` (via OpenAI API).
* **Vector DB**: Qdrant Cloud (via `QDRANT_URL` and `QDRANT_API_KEY`).
* **Source Folder**: [00_Docs/RAG_Data/01_Embed_Ready](file:///home/ubuntu/Ayushi/SantumAI/00_Docs/RAG_Data/01_Embed_Ready) (contains the 11 JSON files).

> [!IMPORTANT]
> **Rate Limits & API Quotas**: To respect API rate limits and prevent `429 Too Many Requests` errors from the embedding provider, the script **must** adhere to the rate-limiting settings defined in `Settings`:
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
   * Send the `content` strings to the OpenAI Embedding API in batches of 5.
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
from qdrant_client.models import Distance, VectorParams, PointStruct, PayloadSchemaType
from openai import OpenAI
from app.core.config import settings

def run_embedding_pipeline():
    # 1. Initialize Clients
    qdrant = QdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY)
    openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    # 2. Reset Qdrant Collection
    qdrant.recreate_collection(
        collection_name=settings.COLLECTION_NAME,
        vectors_config=VectorParams(size=1536, distance=Distance.COSINE) # OpenAI text-embedding-3-small embeds are 1536 dimensions
    )
    
    # 2b. Create Required Payload Indexes for Filtering
    qdrant.create_payload_index(
        collection_name=settings.COLLECTION_NAME,
        field_name="metadata.source",
        field_schema=PayloadSchemaType.KEYWORD
    )
    qdrant.create_payload_index(
        collection_name=settings.COLLECTION_NAME,
        field_name="metadata.is_cbt_manual",
        field_schema=PayloadSchemaType.BOOL
    )
    qdrant.create_payload_index(
        collection_name=settings.COLLECTION_NAME,
        field_name="metadata.chunk_type",
        field_schema=PayloadSchemaType.KEYWORD
    )
    qdrant.create_payload_index(
        collection_name=settings.COLLECTION_NAME,
        field_name="metadata.domain",
        field_schema=PayloadSchemaType.KEYWORD
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
        
        # Call OpenAI Embedding API
        response = openai_client.embeddings.create(
            input=texts,
            model="text-embedding-3-small"
        )
        embeddings = [emb.embedding for emb in response.data]
        
        # Prepare Points for Qdrant
        points = []
        for idx, item in enumerate(batch):
            # Prune and nest metadata to align with VectorDBService/QdrantVectorStore expectations
            payload = {
                "page_content": item["content"],
                "metadata": {
                    "id": item["id"],
                    "chunk_type": item.get("chunk_type", "N/A"),
                    "domain": item.get("domain", "N/A"),
                    "topic": item.get("topic", "N/A"),
                    "source_file": item.get("source_file", "N/A"),
                    "source_family": item.get("source_family", "N/A"),
                    "risk_level": item.get("risk_level", "low"),
                    "source": item.get("source_file", "N/A"),
                    "is_cbt_manual": True # Default True for workbook data, False for FAQ
                }
            }
            
            points.append(PointStruct(
                id=hash(item["id"]) % (10**10), # Numeric ID format for Qdrant
                vector=embeddings[idx],
                payload=payload
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
