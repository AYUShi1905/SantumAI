from typing import Tuple, Optional
import json
import logging
from langchain_groq import ChatGroq
from core.config import settings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

logger = logging.getLogger(__name__)

class ModerationService:
    """
    Service to detect abusive or unsafe content in user messages.
    Uses GPT-OSS-Safeguard-20B for policy-based moderation.
    """

    def __init__(self):
        self.llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model_name=settings.GROQ_MODEL_MODERATION,
            temperature=0,
            max_tokens=500  # Allowing some tokens for reasoning if needed
        )
        
        self.system_policy = (
            "Task: Check if the user message violates the safety policy below.\n\n"
            "SAFETY CATEGORIES:\n"
            "1. Violence & Physical Harm: Threats, glorification of violence, or self-harm.\n"
            "2. Hate Speech: Discrimination based on race, religion, sexual orientation, etc.\n"
            "3. Harassment: Severe verbal abuse or sexual harassment directed at the AI.\n"
            "4. Sexual Content: Explicit or non-consensual sexual content.\n"
            "5. Illegal Acts: Promoting or providing instructions for illegal activities.\n\n"
            "OUTPUT FORMAT:\n"
            "Return a JSON object with two fields:\n"
            "- \"safe\": boolean (true if the message is safe, false if it violates any category)\n"
            "- \"category\": string (the name of the violated category, or \"None\" if safe)\n\n"
            "Return ONLY the JSON object."
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_policy),
            ("human", "{input}")
        ])
        
        self.chain = self.prompt | self.llm | StrOutputParser()

    async def check_message(self, message: str) -> Tuple[bool, Optional[str]]:
        """
        Analyzes a message for safety.
        Returns: (is_safe, category_name)
        """
        try:
            result = await self.chain.ainvoke(
                {"input": message},
                config={"run_name": "SafetyGuard"}
            )
            
            # Clean up result in case model adds markdown formatting
            clean_result = result.strip()
            if clean_result.startswith("```json"):
                clean_result = clean_result.replace("```json", "").replace("```", "").strip()
            
            data = json.loads(clean_result)
            is_safe = data.get("safe", True)
            category = data.get("category", "None")
            
            return is_safe, category if category != "None" else None

        except Exception as e:
            logger.error(f"Moderation Error: {e}")
            # Fail-open for availability (as per proposal standard, or adjust to fail-closed)
            return True, None
