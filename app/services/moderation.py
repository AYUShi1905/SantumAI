from typing import Tuple, Optional
import json
import logging
import re
from langchain_groq import ChatGroq
from core.config import settings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from services.prompt_builder import SystemPromptBuilder

logger = logging.getLogger(__name__)

class ModerationService:
    """
    Service to detect abusive or unsafe content in user messages.
    Uses GPT-OSS-Safeguard-20B for policy-based moderation.
    """

    # LAYER 1: Fast deterministic rules based on client's rule_engine_safety_pack.json
    # Refined to prevent false positives (e.g., "my job is in danger")
    DETERMINISTIC_RULES = {
        "Crisis & Life Threatening": re.compile(
            r"\b(i (want to|might|will) (suicide|kill myself|hurt myself|end my life|die)|i am in danger|i'm in danger)\b", re.IGNORECASE
        ),
        "Severe Mental Symptoms": re.compile(
            r"\b(i am (hearing voices|hallucinating)|i have delusions|i'm losing touch with reality)\b", re.IGNORECASE
        ),
        "Minor Policy": re.compile(
            r"\b(i am (under 18|a minor)|i'm (1[0-7]|[1-9])( years old)?|therapy for my (child|son|daughter))\b", re.IGNORECASE
        ),
        "Medical & Medication": re.compile(
            r"\b((can you|please) (prescribe|diagnose|give me a diagnosis)|what (medication|pills) should i take)\b", re.IGNORECASE
        ),
        "Privacy & Legal": re.compile(
            r"\b(delete my (data|account)|what are my (legal|popia) rights)\b", re.IGNORECASE
        )
    }

    def __init__(self):
        self.llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model_name=settings.GROQ_MODEL_MODERATION,
            temperature=0,
            max_tokens=500  # Allowing some tokens for reasoning if needed
        )
        
        self.system_policy = SystemPromptBuilder.get_moderation_policy()
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_policy),
            ("human", "{input}")
        ])
        
        self.chain = (self.prompt | self.llm | StrOutputParser()).with_config({"run_name": "ModerationChain"})

    async def check_message(self, message: str) -> Tuple[bool, Optional[str]]:
        """
        Analyzes a message for safety.
        Returns: (is_safe, category_name)
        """
        # LAYER 1: Fast Deterministic Rule Engine
        for category, pattern in self.DETERMINISTIC_RULES.items():
            if pattern.search(message):
                logger.info(f"Deterministic safety rule triggered: {category}")
                return False, category

        # LAYER 2: AI Moderation (Fallback for complex nuances)
        try:
            result = await self.chain.ainvoke(
                {"input": message}
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

    async def create_empathetic_refusal(self, category: str, user_message: str):
        """
        Generates a warm, companion-like refusal message based on client-approved safety rules.
        For Crisis (Rule 001), it uses the mandatory template word-for-word.
        """
        
        if category == "Crisis & Life Threatening":
            yield SystemPromptBuilder.get_crisis_template()
            return

        refusal_system_prompt = SystemPromptBuilder.get_refusal_prompt(category)

        try:
            prompt = ChatPromptTemplate.from_messages([
                ("system", refusal_system_prompt),
                ("human", "User message: {input}")
            ])
            chain = (prompt | self.llm | StrOutputParser()).with_config({"run_name": "EmpatheticRefusalChain"})
            
            async for chunk in chain.astream({"input": user_message}):
                yield chunk
        except Exception as e:
            logger.error(f"Error generating empathetic refusal: {e}")
            yield "I hear that you're going through something difficult, but I'm unable to discuss that specific topic. I'm here to support you in any way I can. For professional support, please visit [Santum.net](https://Santum.net)."
