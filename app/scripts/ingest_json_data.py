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
        self.results = []
        
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
        
        status = "Success"
        error_message = None
        total_raw = 0
        skipped_no_content = 0
        restricted_count = 0
        free_allowed_count = 0
        defaulted_domains = 0
        defaulted_chunk_types = 0
        ingested = 0

        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            self.results.append({
                "filename": filename,
                "status": "Failed (File Not Found)",
                "error": f"Path '{file_path}' does not exist.",
                "total_raw": 0,
                "skipped": 0,
                "restricted": 0,
                "allowed": 0,
                "defaulted_domains": 0,
                "defaulted_chunk_types": 0,
                "ingested": 0
            })
            return

        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                total_raw = len(data)
                logger.info(f"Loaded {total_raw} raw items from {filename}")
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON file {filename}: {e}")
                self.results.append({
                    "filename": filename,
                    "status": "Failed (JSON Parse Error)",
                    "error": str(e),
                    "total_raw": 0,
                    "skipped": 0,
                    "restricted": 0,
                    "allowed": 0,
                    "defaulted_domains": 0,
                    "defaulted_chunk_types": 0,
                    "ingested": 0
                })
                return

        documents = []

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
        logger.info(f"  - Total raw items: {total_raw}")
        logger.info(f"  - Skipped (missing content): {skipped_no_content}")
        logger.info(f"  - Flagged as RESTRICTED (paid tier): {restricted_count}")
        logger.info(f"  - Flagged as ALLOWED (free tier): {free_allowed_count}")
        logger.info(f"  - Defaulted missing domains to 'platform': {defaulted_domains}")
        logger.info(f"  - Defaulted missing chunk_types to 'psychoeducation': {defaulted_chunk_types}")
        logger.info(f"  - Prepared {len(documents)} docs for Qdrant storage.")

        if not documents:
            logger.warning(f"No valid documents prepared from {filename}. Skipping DB update.")
            self.results.append({
                "filename": filename,
                "status": "Skipped (No Docs)",
                "error": None,
                "total_raw": total_raw,
                "skipped": skipped_no_content,
                "restricted": restricted_count,
                "allowed": free_allowed_count,
                "defaulted_domains": defaulted_domains,
                "defaulted_chunk_types": defaulted_chunk_types,
                "ingested": 0
            })
            return

        # 5. Add to Vector DB (Uses staged ingestion with rate limiting)
        logger.info(f"Sending {len(documents)} documents to Qdrant collection...")
        try:
            await self.vector_db.add_documents(documents)
            ingested = len(documents)
            logger.info(f"=== Completed Ingestion for: {filename} ===")
            self.results.append({
                "filename": filename,
                "status": "Success",
                "error": None,
                "total_raw": total_raw,
                "skipped": skipped_no_content,
                "restricted": restricted_count,
                "allowed": free_allowed_count,
                "defaulted_domains": defaulted_domains,
                "defaulted_chunk_types": defaulted_chunk_types,
                "ingested": ingested
            })
        except Exception as e:
            logger.error(f"Error adding documents to vector DB for {filename}: {e}")
            self.results.append({
                "filename": filename,
                "status": "Failed (DB Error)",
                "error": str(e),
                "total_raw": total_raw,
                "skipped": skipped_no_content,
                "restricted": restricted_count,
                "allowed": free_allowed_count,
                "defaulted_domains": defaulted_domains,
                "defaulted_chunk_types": defaulted_chunk_types,
                "ingested": 0
            })

    def generate_report(self):
        """Generates and prints a consolidated final report of the ingestion run."""
        report_lines = []
        report_lines.append("="*80)
        report_lines.append("                  FINAL DATA INGESTION REPORT")
        report_lines.append("="*80)
        
        total_files = len(self.results)
        successful_files = sum(1 for r in self.results if r["status"] == "Success")
        failed_files = sum(1 for r in self.results if "Failed" in r["status"])
        skipped_files = sum(1 for r in self.results if "Skipped" in r["status"])

        report_lines.append(f"Files Processed: {total_files}")
        report_lines.append(f"  - Successful:  {successful_files}")
        report_lines.append(f"  - Failed:      {failed_files}")
        report_lines.append(f"  - Skipped:     {skipped_files}")
        report_lines.append("-" * 80)
        
        # Table Header
        report_lines.append(f"{'Filename':<45} | {'Status':<15} | {'Raw':<6} | {'Ingested':<8} | {'Restr.':<6}")
        report_lines.append("-" * 80)
        
        grand_raw = 0
        grand_skipped = 0
        grand_restricted = 0
        grand_allowed = 0
        grand_defaulted_domains = 0
        grand_defaulted_chunk_types = 0
        grand_ingested = 0

        for r in self.results:
            filename_trunc = r["filename"] if len(r["filename"]) <= 45 else r["filename"][:42] + "..."
            status_str = r["status"]
            report_lines.append(
                f"{filename_trunc:<45} | {status_str:<15} | {r['total_raw']:<6} | {r['ingested']:<8} | {r['restricted']:<6}"
            )
            if r["error"]:
                report_lines.append(f"   --> Error Details: {r['error']}")
                
            grand_raw += r["total_raw"]
            grand_skipped += r["skipped"]
            grand_restricted += r["restricted"]
            grand_allowed += r["allowed"]
            grand_defaulted_domains += r["defaulted_domains"]
            grand_defaulted_chunk_types += r["defaulted_chunk_types"]
            grand_ingested += r["ingested"]

        report_lines.append("-" * 80)
        report_lines.append("GRAND TOTALS:")
        report_lines.append(f"  - Total Raw Items Loaded:            {grand_raw}")
        report_lines.append(f"  - Total Skipped (Missing Content):    {grand_skipped}")
        report_lines.append(f"  - Total Flagged as Restricted (Paid): {grand_restricted}")
        report_lines.append(f"  - Total Flagged as Allowed (Free):   {grand_allowed}")
        report_lines.append(f"  - Total Defaulted Domains:           {grand_defaulted_domains}")
        report_lines.append(f"  - Total Defaulted Chunk Types:       {grand_defaulted_chunk_types}")
        report_lines.append(f"  - Total Successfully Ingested:       {grand_ingested}")
        report_lines.append("="*80)
        
        report_content = "\n".join(report_lines)
        print(report_content)
        logger.info("Ingestion complete. Detailed report printed above.")

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

    # Output the final consolidation report
    ingestor.generate_report()

if __name__ == "__main__":
    asyncio.run(main())
