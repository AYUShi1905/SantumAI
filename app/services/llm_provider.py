from langchain_groq import ChatGroq
from app.core.config import settings
from typing import Optional

class LLMProviderService:
    """
    Service responsible for providing and configuring LLM instances.
    Handles routing between simple (8B) and reasoning (70B) models.
    """

    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.simple_model = settings.GROQ_MODEL_SIMPLE
        self.reasoning_model = settings.GROQ_MODEL_REASONING

    def get_llm(self, use_reasoning: bool = False, streaming: bool = True) -> ChatGroq:
        """
        Returns a configured ChatGroq instance.
        
        Args:
            use_reasoning: If True, uses the Llama 3 70B model; otherwise 8B.
            streaming: Whether to enable streaming responses.
        """
        model_name = self.reasoning_model if use_reasoning else self.simple_model
        
        return ChatGroq(
            api_key=self.api_key,
            model_name=model_name,
            streaming=streaming,
            temperature=0.7, # Default temperature for counseling
            max_tokens=1024  # Capped based on project requirements (approx 250 words)
        )
