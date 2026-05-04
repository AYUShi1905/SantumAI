from typing import Literal, Tuple, Dict, Any, Optional
import json
import logging
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from core.config import settings

logger = logging.getLogger(__name__)

class RouterService:
    """
    Service to classify user queries and route them to the appropriate LLM model,
    while also generating a standalone rephrased query in a single pass.
    """

    def __init__(self):
        # Use the fast/cheap model for classification and rephrasing
        self.classifier_llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model_name=settings.GROQ_MODEL_SIMPLE,
            temperature=0,
            max_tokens=500
        )
        
        self.system_prompt = (
            "You are a routing and rephrasing assistant for Santum AI, an emotional-wellbeing counselor.\n"
            "Your task is twofold:\n"
            "1. CLASSIFY: Determine if the message is 'simple' (greetings, FAQ, basic info) or 'complex' (emotional support, counseling, deep reasoning).\n"
            "2. REPHRASE: Based on the chat history and the latest message, formulate a standalone question that can be understood without the chat history. If the query is already standalone, return it as is.\n\n"
            "OUTPUT FORMAT:\n"
            "Return ONLY a JSON object with two fields:\n"
            "- \"classification\": \"simple\" | \"complex\"\n"
            "- \"standalone_query\": \"string\"\n\n"
            "Return ONLY the JSON object."
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}")
        ])
        
        self.chain = self.prompt | self.classifier_llm | StrOutputParser()

    async def process_query(self, message: str, chat_history: list = [], history_summary: Optional[str] = None) -> Tuple[Literal["simple", "complex"], str]:
        """
        Classifies the message and generates a standalone query in a single LLM call.
        Returns: (classification, standalone_query)
        """
        try:
            # Prepare inputs with history summary if available
            inputs = {"input": message, "chat_history": chat_history}
            
            # If we have a summary, we could potentially inject it into the system prompt or as a message
            # For now, let's keep it simple as per the current LangChain flow
            
            result = await self.chain.ainvoke(
                inputs,
                config={"run_name": "QueryProcessor"}
            )
            
            # Clean up result in case model adds markdown formatting
            clean_result = result.strip()
            if clean_result.startswith("```json"):
                clean_result = clean_result.replace("```json", "").replace("```", "").strip()
            
            data = json.loads(clean_result)
            classification = data.get("classification", "simple").lower()
            standalone_query = data.get("standalone_query", message)
            
            return classification if classification in ["simple", "complex"] else "simple", standalone_query
            
        except Exception as e:
            logger.error(f"Router/Rephraser Error: {e}")
            # Default to simple and original message on error
            return "simple", message
