from typing import Literal
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from core.config import settings

class RouterService:
    """
    Service to classify user queries and route them to the appropriate LLM model.
    """

    def __init__(self):
        # Use the fast/cheap model for classification
        self.classifier_llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model_name=settings.GROQ_MODEL_SIMPLE,
            temperature=0,
            max_tokens=10
        )
        
        self.system_prompt = (
            "You are a routing assistant. Your task is to classify a user's message into one of two categories:\n"
            "1. 'simple': Greetings, Santum AI/PWA info, simple questions, coping tips, or general FAQ.\n"
            "2. 'complex': Deeper conversations, emotional context, complex reasoning, or specific counseling needs.\n\n"
            "Output ONLY the word 'simple' or 'complex'. Do not explain."
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", "{input}")
        ])
        
        self.chain = self.prompt | self.classifier_llm | StrOutputParser()

    async def classify(self, message: str) -> Literal["simple", "complex"]:
        """
        Classifies the message to determine if it needs a reasoning model.
        """
        try:
            result = await self.chain.ainvoke({"input": message})
            label = result.strip().lower()
            if "complex" in label:
                return "complex"
            return "simple"
        except Exception:
            # Default to simple on error to save costs/latency
            return "simple"
