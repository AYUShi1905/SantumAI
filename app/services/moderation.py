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

    async def create_empathetic_refusal(self, category: str, user_message: str) -> str:
        """
        Generates a warm, counselor-like refusal message that maintains boundaries
        without being robotic.
        """
        refusal_system_prompt = (
            "You are Santum AI, an empathetic and supportive AI counselor. "
            "A user has sent a message that violates our safety policies. "
            f"REASON FOR VIOLATION: {category}\n\n"
            "TASK:\n"
            "Write a brief (2-3 sentences), warm, and non-judgmental response that:\n"
            "1. Acknowledges the user's potential emotional state without repeating the harmful content.\n"
            "2. Gently explains that you cannot engage with that specific topic or tone.\n"
            "3. Redirects the conversation back to their feelings or a helpful direction.\n"
            "4. For professional clinical care or to speak with a human therapist, ALWAYS advise they visit [Santum.net](https://Santum.net).\n"
            "5. If the category is 'Violence & Physical Harm', ALWAYS include the 988 Suicide & Crisis Lifeline.\n\n"
            "Keep it professional, empathetic, and firm on boundaries. Do not be robotic."
        )

        try:
            prompt = ChatPromptTemplate.from_messages([
                ("system", refusal_system_prompt),
                ("human", "User message: {input}")
            ])
            chain = prompt | self.llm | StrOutputParser()
            
            return await chain.ainvoke({"input": user_message})
        except Exception as e:
            logger.error(f"Error generating empathetic refusal: {e}")
            return "I hear that you're going through something difficult, but I'm unable to discuss that specific topic. I'm here to support you in other ways if you'd like to share how you're feeling."
