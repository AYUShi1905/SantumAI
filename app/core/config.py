from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # Qdrant Vector DB
    QDRANT_API_KEY: str
    QDRANT_URL: str
    COLLECTION_NAME: str

    # Jina Cloud Embeddings
    JINA_API_KEY: str
    JINA_EMBEDDING_URL: str = "https://api.jina.ai/v1/embeddings"
    JINA_EMBEDDING_MODEL: str = "jina-embeddings-v2-base-en"

    # Groq LLMs
    GROQ_API_KEY: str
    GROQ_MODEL_SIMPLE: str = "llama3-8b-8192"
    GROQ_MODEL_REASONING: str = "llama3-70b-8192"

    # App Settings
    PROJECT_NAME: str = "Santum AI RAG Service"
    DEBUG: bool = False

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
