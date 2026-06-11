import os
import sys
import json
import asyncio
import logging
from typing import List

# Add app directory to path to allow importing services
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
app_dir = os.path.join(project_root, "app")

sys.path.append(app_dir)
os.chdir(project_root) # Ensure relative paths to JSON files work

# Load environment variables from app/.env
from dotenv import load_dotenv
load_dotenv(os.path.join(app_dir, ".env"))

from services.vector_db import VectorDBService
from langchain_core.documents import Document

# Initialize Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("JSONIngestor")

class JSONIngestor:
    def __init__(self):
        self.vector_db = VectorDBService()

    async def ingest_json(self, file_path: str, is_cbt_manual: bool):
        """Parses and ingests a specific JSON RAG index file."""
        filename = os.path.basename(file_path)
        logger.info(f"--- Starting ingestion for: {filename} ---")
        
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return

        with open(file_path, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON: {e}")
                return

        documents = []
        for item in data:
            # 1. Validation Logic
            # For GAD data: safety.embed_allowed must be true
            # For Platform data: embedding_approved must be true
            if is_cbt_manual:
                allowed = item.get("safety", {}).get("embed_allowed", False)
            else:
                allowed = item.get("embedding_approved", False)

            if not allowed:
                continue

            # 2. Extract content and metadata
            content = item.get("embedding_text")
            if not content:
                logger.warning(f"Item {item.get('id')} missing 'embedding_text'. Skipping.")
                continue

            # 3. Build Metadata
            # We preserve original fields but ensure 'source' and 'is_cbt_manual' are set correctly
            metadata = {k: v for k, v in item.items() if k != "embedding_text"}
            metadata["source"] = filename
            metadata["is_cbt_manual"] = is_cbt_manual

            # 4. Create LangChain Document
            doc = Document(page_content=content, metadata=metadata)
            documents.append(doc)

        if not documents:
            logger.warning(f"No valid documents found in {filename}")
            return

        logger.info(f"Prepared {len(documents)} documents from {filename}. Sending to Vector DB...")
        
        # 5. Add to Vector DB (Uses staged ingestion with rate limiting)
        await self.vector_db.add_documents(documents)
        logger.info(f"--- Completed ingestion for: {filename} ---")

async def main():
    ingestor = JSONIngestor()
    
    # Define files to ingest
    tasks = [
        {
            "path": "00_Docs/Data_by_client/santum_ai_vector_embedding_index.json",
            "is_cbt_manual": False
        },
        {
            "path": "new-data-by-client/santum_ai_cbt_gad_vector_index_v2.json",
            "is_cbt_manual": True
        }
    ]
    
    # Process sequentially to avoid overlapping rate limit delays
    for task in tasks:
        await ingestor.ingest_json(task["path"], task["is_cbt_manual"])

if __name__ == "__main__":
    asyncio.run(main())
