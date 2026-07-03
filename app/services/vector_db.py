from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.http import models as rest
from core.config import settings
from typing import List
from langchain_core.documents import Document

class VectorDBService:
    """
    Service for interacting with Qdrant Vector Database.
    Uses OpenAI (text-embedding-3-small) for generating embeddings.
    """

    def __init__(self):
        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY
        )
        self.embeddings = OpenAIEmbeddings(
            model=settings.OPENAI_EMBEDDING_MODEL,
            openai_api_key=settings.OPENAI_API_KEY
        )
        # Set custom name for LangSmith tracing
        try:
            self.embeddings.name = "OpenAIEmbedder"
        except Exception:
            pass
        self.collection_name = settings.COLLECTION_NAME
        self._ensure_collection_exists()

    def _ensure_collection_exists(self):
        """Checks if collection exists, if not, creates it with correct dimensions and indexes."""
        try:
            collections = self.client.get_collections().collections
            exists = any(c.name == self.collection_name for c in collections)
            
            if exists:
                collection_info = self.client.get_collection(self.collection_name)
                vectors_config = collection_info.config.params.vectors
                if hasattr(vectors_config, "size"):
                    existing_size = vectors_config.size
                elif isinstance(vectors_config, dict) and "size" in vectors_config:
                    existing_size = vectors_config["size"]
                else:
                    existing_size = None
                
                # Check for required indexes in the payload schema
                payload_schema = collection_info.payload_schema or {}
                required_indexes = ["metadata.source", "metadata.is_cbt_manual", "metadata.chunk_type", "metadata.domain"]
                has_all_indexes = all(idx in payload_schema for idx in required_indexes)
                
                if (existing_size and existing_size != 1536) or not has_all_indexes:
                    print(f"Collection {self.collection_name} mismatch (size: {existing_size}, indexes: {list(payload_schema.keys())}). Deleting and recreating...")
                    self.client.delete_collection(self.collection_name)
                    exists = False
            
            if not exists:
                # OpenAI text-embedding-3-small uses 1536 dimensions
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=rest.VectorParams(
                        size=1536, 
                        distance=rest.Distance.COSINE
                    )
                )
                
                # Create payload index for the 'source' field to allow efficient deletion/filtering
                self.client.create_payload_index(
                    collection_name=self.collection_name,
                    field_name="metadata.source",
                    field_schema=rest.PayloadSchemaType.KEYWORD
                )
                
                # Create payload index for 'is_cbt_manual' for plan-based filtering
                self.client.create_payload_index(
                    collection_name=self.collection_name,
                    field_name="metadata.is_cbt_manual",
                    field_schema=rest.PayloadSchemaType.BOOL
                )
                
                # Create payload index for 'chunk_type' for tier restriction filtering
                self.client.create_payload_index(
                    collection_name=self.collection_name,
                    field_name="metadata.chunk_type",
                    field_schema=rest.PayloadSchemaType.KEYWORD
                )
                
                # Create payload index for 'domain' for domain-based retrieval filtering
                self.client.create_payload_index(
                    collection_name=self.collection_name,
                    field_name="metadata.domain",
                    field_schema=rest.PayloadSchemaType.KEYWORD
                )
        except Exception as e:
            # Log error or handle as needed
            print(f"Error ensuring collection exists: {e}")

    def get_vectorstore(self) -> QdrantVectorStore:
        """Returns a LangChain compatible Qdrant vectorstore instance."""
        return QdrantVectorStore(
            client=self.client,
            collection_name=self.collection_name,
            embedding=self.embeddings
        )

    async def similarity_search(self, query: str, k: int = 5) -> List[Document]:
        """Performs a semantic search in the vector database."""
        vectorstore = self.get_vectorstore()
        return await vectorstore.asimilarity_search(query, k=k)

    async def add_documents(self, documents: List[Document]):
        """
        Adds a list of LangChain documents to the vector store in stages.
        Uses batching, delays, and retries to handle Google Gemini API rate limits.
        """
        import asyncio
        import logging
        logger = logging.getLogger(__name__)

        vectorstore = self.get_vectorstore()
        batch_size = settings.EMBEDDING_BATCH_SIZE
        delay = settings.EMBEDDING_DELAY_SECONDS
        
        total_docs = len(documents)
        total_batches = (total_docs + batch_size - 1) // batch_size
        
        start_msg = f"Starting staged ingestion: {total_docs} docs, {total_batches} batches (Size: {batch_size}, Delay: {delay}s)"
        logger.info(start_msg)

        for i in range(0, total_docs, batch_size):
            batch = documents[i : i + batch_size]
            current_batch_num = (i // batch_size) + 1
            
            # Retry logic for individual batch
            max_retries = 3
            retry_count = 0
            while retry_count <= max_retries:
                try:
                    progress_msg = f"[Batch {current_batch_num}/{total_batches}] Embedding {len(batch)} chunks (Attempt {retry_count + 1})..."
                    logger.info(progress_msg)
                    
                    await vectorstore.aadd_documents(batch)
                    
                    success_msg = f"[Batch {current_batch_num}/{total_batches}] Successfully ingested."
                    logger.info(success_msg)
                    break # Success, exit retry loop
                except Exception as e:
                    error_msg = str(e)
                    if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                        retry_count += 1
                        if retry_count <= max_retries:
                            wait_time = 60 # Wait a full minute on 429 to let quota reset
                            warn_msg = f"[Batch {current_batch_num}/{total_batches}] Rate limit hit. Waiting {wait_time}s before retry {retry_count}/{max_retries}..."
                            logger.warning(warn_msg)
                            await asyncio.sleep(wait_time)
                        else:
                            fail_msg = f"[Batch {current_batch_num}/{total_batches}] Max retries exceeded on 429."
                            logger.error(fail_msg)
                            raise e
                    else:
                        fail_msg = f"[Batch {current_batch_num}/{total_batches}] Non-retryable error: {error_msg}"
                        logger.error(fail_msg)
                        raise e
            
            # Delay between batches, but not after the last batch
            if i + batch_size < total_docs:
                logger.debug(f"Waiting {delay}s to respect rate limits...")
                await asyncio.sleep(delay)
        
        final_msg = f"Successfully ingested all {total_docs} documents in {total_batches} stages."
        logger.info(final_msg)

    def list_ingested_files(self) -> List[str]:
        """Returns a list of unique filenames present in the collection metadata."""
        # Using scroll to get points and extract unique sources
        # Note: For very large collections, this would need pagination
        points, _ = self.client.scroll(
            collection_name=self.collection_name,
            limit=10000, 
            with_payload=True,
            with_vectors=False
        )
        
        sources = set()
        for point in points:
            if point.payload and "metadata" in point.payload:
                source = point.payload["metadata"].get("source")
                if source:
                    sources.add(source)
        
        return sorted(list(sources))

    def delete_by_filename(self, filename: str):
        """Deletes all points associated with a specific filename."""
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=rest.Filter(
                must=[
                    rest.FieldCondition(
                        key="metadata.source",
                        match=rest.MatchValue(value=filename)
                    )
                ]
            )
        )

    def clear_collection(self):
        """Deletes all points in the collection."""
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=rest.Filter(
                must=[] # Empty filter matches everything
            )
        )
