from pydantic import BaseModel, Field
from typing import List, Optional

class ChatMessage(BaseModel):
    role: str = Field(..., description="The role of the message sender (human or ai)")
    content: str = Field(..., description="The actual text content of the message")

class SummarizeRequest(BaseModel):
    chat_history: List[ChatMessage] = Field(..., description="The sequence of messages to summarize")

class ChatRequest(BaseModel):
    query: str
    chat_history: Optional[List[ChatMessage]] = []
    use_reasoning: bool = False
