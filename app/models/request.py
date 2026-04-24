from pydantic import BaseModel, Field
from typing import List, Optional

class ChatMessage(BaseModel):
    role: str = Field(..., description="The role of the message sender (human or ai)")
    content: str = Field(..., description="The actual text content of the message")

class ChatRequest(BaseModel):
    message: str = Field(..., description="The current user message")
    chat_history: List[ChatMessage] = Field(default_factory=list, description="Previous messages in the conversation")
    use_reasoning: bool = Field(default=False, description="Whether to use the more powerful 70B model")

class SummarizeRequest(BaseModel):
    chat_history: List[ChatMessage] = Field(..., description="The sequence of messages to summarize")
