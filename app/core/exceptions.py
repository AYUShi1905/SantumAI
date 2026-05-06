from typing import Any, Dict, Optional

class SantumException(Exception):
    """Base exception for all Santum AI errors."""
    def __init__(self, message: str, status_code: int = 500, detail: Optional[Any] = None):
        self.message = message
        self.status_code = status_code
        self.detail = detail
        super().__init__(self.message)

class LLMProviderError(SantumException):
    """Exception raised when an LLM provider (Groq/OpenAI) fails."""
    def __init__(self, message: str, detail: Optional[Any] = None):
        super().__init__(message, status_code=502, detail=detail)

class VectorDBError(SantumException):
    """Exception raised when Qdrant operations fail."""
    def __init__(self, message: str, detail: Optional[Any] = None):
        super().__init__(message, status_code=503, detail=detail)

class RAGProcessingError(SantumException):
    """Exception raised for errors during the RAG pipeline orchestration."""
    def __init__(self, message: str, detail: Optional[Any] = None):
        super().__init__(message, status_code=500, detail=detail)

class ModerationError(SantumException):
    """Exception raised for errors during the moderation phase."""
    def __init__(self, message: str, detail: Optional[Any] = None):
        super().__init__(message, status_code=500, detail=detail)

class IngestionError(SantumException):
    """Exception raised during document parsing or ingestion."""
    def __init__(self, message: str, detail: Optional[Any] = None):
        super().__init__(message, status_code=422, detail=detail)
