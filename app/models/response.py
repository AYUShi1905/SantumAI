from pydantic import BaseModel
from typing import Optional, List

class IngestResponse(BaseModel):
    message: str
    filename: str
    chunks_processed: int
    status: str = "success"

class SummarizeResponse(BaseModel):
    summary: str
    status: str = "success"

class ErrorResponse(BaseModel):
    detail: str
    status: str = "error"
