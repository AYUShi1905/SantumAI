from langchain_groq import ChatGroq
from core.config import settings
from typing import Optional
from models.request import PlanLevel

class LLMProviderService:
    """
    Service responsible for providing and configuring LLM instances.
    Handles routing between simple (8B) and reasoning (70B) models.
    """

    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        # Aligned with AI Architecture Summary 2.pdf
        self.counseling_model = settings.MODEL_COUNSELING
        self.background_model = settings.MODEL_BACKGROUND

    def get_llm(self, use_reasoning: bool = False, streaming: bool = True) -> ChatGroq:
        """
        Returns a configured ChatGroq instance.
        
        Args:
            use_reasoning: If True, uses the Counseling (70B) model; otherwise Background (8B).
            streaming: Whether to enable streaming responses.
        """
        model_name = self.counseling_model if use_reasoning else self.background_model
        
        # We rely on Prompt Instructions for word limits to avoid cutting off sentences.
        # 1024 is a generous safety limit for all plans.
        max_tokens = 1024
        
        return ChatGroq(
            api_key=self.api_key,
            model_name=model_name,
            streaming=streaming,
            temperature=0.7, # Default temperature for counseling
            max_tokens=max_tokens
        )
