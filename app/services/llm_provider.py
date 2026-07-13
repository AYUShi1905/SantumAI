from langchain_openai import ChatOpenAI
from core.config import settings
from typing import Optional
from models.request import PlanLevel

class LLMProviderService:
    """
    Service responsible for providing and configuring OpenAI ChatOpenAI instances.
    Handles routing between simple and reasoning models.
    """

    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        # Aligned with AI Architecture Summary 2.pdf
        self.counseling_model = settings.MODEL_COUNSELING
        self.background_model = settings.MODEL_BACKGROUND
        self.routing_model = settings.MODEL_ROUTING

    def get_llm(self, use_reasoning: bool = False, streaming: bool = True) -> ChatOpenAI:
        """
        Returns a configured ChatOpenAI instance.
        
        Args:
            use_reasoning: If True, uses the Counseling model; otherwise Background.
            streaming: Whether to enable streaming responses.
        """
        model_name = self.counseling_model if use_reasoning else self.background_model
        
        # We rely on Prompt Instructions for word limits to avoid cutting off sentences.
        # 1024 is a generous safety limit for all plans.
        max_tokens = 1024
        
        return ChatOpenAI(
            api_key=self.api_key,
            model=model_name,
            streaming=streaming,
            temperature=0.7, # Default temperature for counseling
            max_tokens=max_tokens
        )

    def get_routing_llm(self, streaming: bool = True) -> ChatOpenAI:
        """
        Returns a configured ChatOpenAI instance using the routing model (nano).
        """
        return ChatOpenAI(
            api_key=self.api_key,
            model=self.routing_model,
            streaming=streaming,
            temperature=0.7,
            max_tokens=200
        )

