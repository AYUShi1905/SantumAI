from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # Qdrant Vector DB
    QDRANT_API_KEY: str
    QDRANT_URL: str
    COLLECTION_NAME: str

    # Jina Cloud Embeddings (Deprecated)
    JINA_API_KEY: Optional[str] = None
    JINA_EMBEDDING_URL: str = "https://api.jina.ai/v1/embeddings"
    JINA_EMBEDDING_MODEL: str = "jina-embeddings-v2-base-en"

    # Google Gemini Embeddings
    GOOGLE_API_KEY: str
    GOOGLE_EMBEDDING_MODEL: str = "models/gemini-embedding-001"

    # Groq LLMs
    GROQ_API_KEY: str
    GROQ_MODEL_SIMPLE: str = "llama3-8b-8192"
    GROQ_MODEL_REASONING: str = "llama3-70b-8192"
    GROQ_MODEL_MODERATION: str = "openai/gpt-oss-safeguard-20b"

    # App Settings
    PROJECT_NAME: str = "Santum AI RAG Service"
    DEBUG: bool = False

    # LangSmith Tracing
    LANGSMITH_TRACING: bool = False
    LANGSMITH_ENDPOINT: str = "https://api.smith.langchain.com"
    LANGSMITH_API_KEY: Optional[str] = None
    LANGSMITH_PROJECT: str = "santum-ai"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

# Export LangSmith variables to environment for LangChain SDK
import os
if settings.LANGSMITH_TRACING:
    # Legacy/Standard LangChain vars
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_ENDPOINT"] = settings.LANGSMITH_ENDPOINT
    os.environ["LANGCHAIN_API_KEY"] = settings.LANGSMITH_API_KEY or ""
    os.environ["LANGCHAIN_PROJECT"] = settings.LANGSMITH_PROJECT
    # Modern LangSmith vars
    os.environ["LANGSMITH_TRACING"] = "true"
    os.environ["LANGSMITH_ENDPOINT"] = settings.LANGSMITH_ENDPOINT
    os.environ["LANGSMITH_API_KEY"] = settings.LANGSMITH_API_KEY or ""
    os.environ["LANGSMITH_PROJECT"] = settings.LANGSMITH_PROJECT

