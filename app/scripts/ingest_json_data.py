import os
import sys
import json
import asyncio
import logging
from typing import List

# Setup pathing to allow importing modules from the app directory
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
app_dir = os.path.join(project_root, "app")

sys.path.append(app_dir)
os.chdir(project_root)  # Keep working directory consistent

from services.vector_db import VectorDBService
from langchain_core.documents import Document

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("JSONIngestor")

class JSONIngestor:
    def __init__(self):
        logger.info("Initializing JSON Ingestor Service...")
        self.vector_db = VectorDBService()
        self.restricted_ids = set()
        
        # Load restricted chunk IDs from compact list JSON
        restriction_file = os.path.join(
            project_root, 
            "00_Docs", 
            "RAG_Data", 
            "04_Tier_Restrictions", 
            "santum_ai_paid_tier_COMPACT_exercise_worksheet_restriction_list.json"
        )
        
        logger.info(f"Loading restricted chunk IDs from: {restriction_file}")
        if os.path.exists(restriction_file):
            try:
                with open(restriction_file, "r", encoding="utf-8") as rf:
                    restrictions = json.load(rf)
                self.restricted_ids = set(restrictions.get("restricted_chunk_ids", []))
                logger.info(f"Successfully loaded {len(self.restricted_ids)} restricted chunk IDs.")
            except Exception as e:
                logger.error(f"Error reading restricted chunk list: {e}")
        else:
            logger.warning(
                f"Restricted chunk list file not found at: {restriction_file}. "
                "No chunks will be flagged as restricted."
            )

    async def ingest_json(self, file_path: str, is_cbt_manual: bool):
        """Parses and ingests a specific JSON RAG index file into Qdrant."""
        filename = os.path.basename(file_path)
        logger.info(f"=== Starting Ingestion Process for: {filename} ===")
        
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return

        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                logger.info(f"Loaded {len(data)} raw items from {filename}")
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON file {filename}: {e}")
                return

        documents = []
        skipped_no_content = 0
        restricted_count = 0
        free_allowed_count = 0
        defaulted_domains = 0
        defaulted_chunk_types = 0

        for item in data:
            item_id = item.get("id", "N/A")

            # 1. Extract content (using embedding_text as primary document payload)
            content = item.get("embedding_text")
            if not content:
                logger.warning(f"Item {item_id} in {filename} missing 'embedding_text'. Skipping.")
                skipped_no_content += 1
                continue

            # 2. Build Metadata Payload
            # We copy all JSON keys except embedding_text
            metadata = {k: v for k, v in item.items() if k != "embedding_text"}
            metadata["source"] = filename
            metadata["is_cbt_manual"] = is_cbt_manual

            # Default domain if missing (specifically for core FAQ index)
            if "domain" not in metadata:
                metadata["domain"] = "platform"
                defaulted_domains += 1

            # Default chunk_type if missing (specifically for Self-Esteem manual)
            if "chunk_type" not in metadata:
                metadata["chunk_type"] = "psychoeducation"
                defaulted_chunk_types += 1

            # Map the exact is_restricted boolean based on the external JSON set
            if item_id in self.restricted_ids:
                metadata["is_restricted"] = True
                restricted_count += 1
            else:
                metadata["is_restricted"] = False
                free_allowed_count += 1

            # 3. Create LangChain Document
            doc = Document(page_content=content, metadata=metadata)
            documents.append(doc)

        logger.info(f"Ingestion Analysis for {filename}:")
        logger.info(f"  - Total raw items: {len(data)}")
        logger.info(f"  - Skipped (missing content): {skipped_no_content}")
        logger.info(f"  - Flagged as RESTRICTED (paid tier): {restricted_count}")
        logger.info(f"  - Flagged as ALLOWED (free tier): {free_allowed_count}")
        logger.info(f"  - Defaulted missing domains to 'platform': {defaulted_domains}")
        logger.info(f"  - Defaulted missing chunk_types to 'psychoeducation': {defaulted_chunk_types}")
        logger.info(f"  - Prepared {len(documents)} docs for Qdrant storage.")

        if not documents:
            logger.warning(f"No valid documents prepared from {filename}. Skipping DB update.")
            return

        # 5. Add to Vector DB (Uses staged ingestion with rate limiting)
        logger.info(f"Sending {len(documents)} documents to Qdrant collection...")
        await self.vector_db.add_documents(documents)
        logger.info(f"=== Completed Ingestion for: {filename} ===")

async def main():
    ingestor = JSONIngestor()
    
    # Define files to ingest
    tasks = [
        # Platform FAQ Data (Non-CBT)
        {
            "path": "00_Docs/RAG_Data/01_Embed_Ready/santum_ai_vector_embedding_index.json",
            "is_cbt_manual": False
        },
        # CBT Workbook Data
        {
            "path": "00_Docs/RAG_Data/01_Embed_Ready/santum_ai_cbt_gad_vector_index_v1_EMBED_READY.json",
            "is_cbt_manual": True
        },
        {
            "path": "00_Docs/RAG_Data/01_Embed_Ready/santum_ai_cbt_assertiveness_vector_index_v1_EMBED_READY.json",
            "is_cbt_manual": True
        },
        {
            "path": "00_Docs/RAG_Data/01_Embed_Ready/santum_ai_cbt_bipolar_support_vector_index_v1_EMBED_READY.json",
            "is_cbt_manual": True
        },
        {
            "path": "00_Docs/RAG_Data/01_Embed_Ready/santum_ai_cbt_body_acceptance_vector_index_v1_EMBED_READY.json",
            "is_cbt_manual": True
        },
        {
            "path": "00_Docs/RAG_Data/01_Embed_Ready/santum_ai_cbt_body_image_vector_index_v1_EMBED_READY.json",
            "is_cbt_manual": True
        },
        {
            "path": "00_Docs/RAG_Data/01_Embed_Ready/santum_ai_cbt_depression_vector_index_v1_EMBED_READY.json",
            "is_cbt_manual": True
        },
        {
            "path": "00_Docs/RAG_Data/01_Embed_Ready/santum_ai_cbt_eating_disorder_recovery_vector_index_v1_EMBED_READY.json",
            "is_cbt_manual": True
        },
        {
            "path": "00_Docs/RAG_Data/01_Embed_Ready/santum_ai_cbt_panic_vector_index_v3_EMBED_READY.json",
            "is_cbt_manual": True
        },
        {
            "path": "00_Docs/RAG_Data/01_Embed_Ready/santum_ai_cbt_self_esteem_vector_index_v1_EMBED_READY.json",
            "is_cbt_manual": True
        },
        {
            "path": "00_Docs/RAG_Data/01_Embed_Ready/santum_ai_cbt_social_anxiety_vector_index_v1_EMBED_READY.json",
            "is_cbt_manual": True
        }
    ]
    
    # Process sequentially to avoid overlapping rate limit delays
    for task in tasks:
        await ingestor.ingest_json(task["path"], task["is_cbt_manual"])

if __name__ == "__main__":
    asyncio.run(main())
