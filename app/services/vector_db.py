from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings import JinaEmbeddings
from qdrant_client import QdrantClient
from app.core.config import settings
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
        self.collection_name = settings.COLLECTION_NAME

    def get_vectorstore(self) -> Qdrant:
        """Returns a LangChain compatible Qdrant vectorstore instance."""
        return Qdrant(
            client=self.client,
            collection_name=self.collection_name,
            embeddings=self.embeddings
        )

    async def similarity_search(self, query: str, k: int = 5) -> List[Document]:
        """Performs a semantic search in the vector database."""
        vectorstore = self.get_vectorstore()
        return await vectorstore.asimilarity_search(query, k=k)

    def add_documents(self, documents: List[Document]):
        """Adds a list of LangChain documents to the vector store."""
        Qdrant.from_documents(
            documents,
            self.embeddings,
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
            collection_name=self.collection_name
        )
