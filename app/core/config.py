from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # Qdrant Vector DB
    QDRANT_API_KEY: str
    QDRANT_URL: str
    COLLECTION_NAME: str

    # Google Gemini Embeddings
    GOOGLE_API_KEY: str
    GOOGLE_EMBEDDING_MODEL: str = "gemini-embedding-001"

    MODEL_COUNSELING: str = "llama-3.3-70b-versatile"  # Main counselling response (GPT-4.1 in Production)
    MODEL_BACKGROUND: str = "llama-3.1-8b-instant"   # Summarization, memory, moderation (GPT-4.1 Mini in Production)
    MODEL_ROUTING: str = "llama-3.1-8b-instant"      # Tags, routing, analytics (GPT-4.1 Nano in Production)

    # Groq LLMs (Legacy - Keeping for backward compatibility temporarily)
    GROQ_API_KEY: str
    GROQ_MODEL_MODERATION: str = "llama-3.1-8b-instant" # Safety classification (GPT-4.1 Mini in Production)

    # App Settings
    PROJECT_NAME: str = "Santum AI RAG Service"
    DEBUG: bool = False

    # LangSmith Tracing
    LANGSMITH_TRACING: bool = False
    LANGSMITH_ENDPOINT: str = "https://api.smith.langchain.com"
    LANGSMITH_API_KEY: Optional[str] = None
    LANGSMITH_PROJECT: str = "santum-ai"

    # Embedding Rate Limiting
    EMBEDDING_BATCH_SIZE: int = 5
    EMBEDDING_DELAY_SECONDS: float = 10.0

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

