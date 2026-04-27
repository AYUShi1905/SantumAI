from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class PlanLevel(str, Enum):
    FREE = "free"
    STANDARD = "standard"
    PREMIUM = "premium"

class ChatMessage(BaseModel):
    role: str = Field(..., description="The role of the message sender (human or ai)")
    content: str = Field(..., description="The actual text content of the message")

class ChatRequest(BaseModel):
    message: str = Field(..., description="The current user message")
    chat_history: List[ChatMessage] = Field(default_factory=list, description="Previous messages in the conversation (last few full messages)")
    history_summary: Optional[str] = Field(default=None, description="A summary of older parts of the conversation")
    plan_level: PlanLevel = Field(default=PlanLevel.FREE, description="The user's subscription plan")
    use_reasoning: Optional[bool] = Field(default=None, description="Override the automatic model router if provided")
    remaining_tokens: int = Field(default=0, description="The number of tokens the user has left in their balance")

class SummarizeRequest(BaseModel):
    chat_history: List[ChatMessage] = Field(..., description="The sequence of messages to summarize")
    existing_summary: Optional[str] = Field(default=None, description="Previous summary to be extended with new history")
