from langchain_qdrant import QdrantVectorStore
from langchain_community.embeddings import JinaEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.http import models as rest
from core.config import settings
from typing import List
from langchain_core.documents import Document

class VectorDBService:
    """
    Service for interacting with Qdrant Vector Database.
    Uses Jina v2-base-en for generating embeddings.
    """

    def __init__(self):
        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY
        )
        self.embeddings = JinaEmbeddings(
            jina_api_key=settings.JINA_API_KEY,
            model_name=settings.JINA_EMBEDDING_MODEL
        )
        # Set custom name for LangSmith tracing
        self.embeddings.model_name = settings.JINA_EMBEDDING_MODEL 
        # Note: LangChain components often use the 'name' attribute for tracing
        try:
            self.embeddings.name = "JinaVectorEmbedder"
        except Exception:
            pass
        self.collection_name = settings.COLLECTION_NAME
        self._ensure_collection_exists()

    def _ensure_collection_exists(self):
        """Checks if collection exists, if not, creates it with correct dimensions and indexes."""
        try:
            collections = self.client.get_collections().collections
            exists = any(c.name == self.collection_name for c in collections)
            
            if not exists:
                # Jina v2-base-en uses 768 dimensions
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=rest.VectorParams(
                        size=768, 
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

    def add_documents(self, documents: List[Document]):
        """Adds a list of LangChain documents to the vector store."""
        vectorstore = self.get_vectorstore()
        vectorstore.add_documents(documents)

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
