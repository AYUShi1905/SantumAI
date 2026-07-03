from typing import Literal, Tuple, Dict, Any, Optional
import json
import logging
from langchain_openai import ChatOpenAI
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
        # Aligned with AI Architecture Summary 2.pdf
        # Use the dedicated routing model
        self.classifier_llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=settings.MODEL_ROUTING,
            temperature=0,
            max_tokens=500,
            model_kwargs={"response_format": {"type": "json_object"}}
        )
        
        self.system_prompt = (
            "You are a routing and rephrasing assistant for Sai (short for Santum AI), an emotional-wellbeing companion.\n"
            "Your task is threefold:\n"
            "1. CLASSIFY: Determine the message type.\n"
            "   - 'greeting': ONLY for pure greetings (hi, hello) or basic acknowledgments (ok, thanks).\n"
            "   - 'conversational': For emotional support, venting, sharing feelings, and general chat where the user does NOT ask for specific tools, exercises, or policies. No RAG is needed here.\n"
            "   - 'rag_required': For EXPLICIT requests for CBT tools, exercises, grounding techniques, Santum platform policies, clinical advice, or Santum AI identity/capabilities (including questions about what Santum is or who created it).\n"
            "2. REPHRASE: Based on the chat history and the latest message, formulate a standalone query that represents the user's intent and can be used for document retrieval. "
            "The query must be from the USER'S perspective (e.g., 'How to manage stress' or 'I am feeling anxious') and NOT an AI response or a question directed at the user. "
            "If the query is already standalone, return it as is.\n"
            "3. CLASSIFY DOMAIN: Determine which specific workbook/domain context this message belongs to. If it's ambiguous, a general greeting, or doesn't map to a specific CBT topic, output 'none'.\n"
            "   Available domains:\n"
            "   - 'cbt_assertiveness': Assertiveness workbook, communication styles, setting boundaries, handling criticism.\n"
            "   - 'cbt_bipolar': Bipolar support, mania, hypomania, depression episodes in bipolar disorder.\n"
            "   - 'cbt_body_acceptance': Body acceptance, body dysmorphic disorder (BDD) workbook.\n"
            "   - 'cbt_body_image': Body image concerns, negative self-image related to appearance.\n"
            "   - 'cbt_depression': Depression workbook, feeling low, lethargic, hopeless, behavioral activation.\n"
            "   - 'cbt_eating_disorder': Eating disorder recovery, purging, bingeing, body-checking, recovery worksheets.\n"
            "   - 'cbt_gad': Generalized anxiety disorder workbook, chronic worrying, worry postponement, what-if thoughts, breathing or grounding exercises.\n"
            "   - 'cbt_panic': Panic workbook, panic attacks, physical anxiety symptoms, hyperventilation, interoceptive exposure, grounding techniques (like 5-4-3-2-1), deep breathing exercises.\n"
            "   - 'cbt_self_esteem': Self-esteem workbook, core beliefs, negative self-talk, self-compassion.\n"
            "   - 'cbt_social_anxiety': Social anxiety workbook, fear of judgment, avoidance of social situations, safety behaviors.\n"
            "   - 'platform': Platform FAQ, Santum Facts, app/service features, therapist details, subscription queries, developer info.\n"
            "   - 'none': Greetings, general chit-chat, ambiguous topic, or general/unrelated counseling query.\n\n"
            "FEW-SHOT EXAMPLES:\n"
            "- Input: 'What is Santum AI?' -> Class: 'rag_required', Domain: 'platform'\n"
            "- Input: 'Who built Santum?' -> Class: 'rag_required', Domain: 'platform'\n"
            "- Input: 'Can you show me a grounding technique?' -> Class: 'rag_required', Domain: 'cbt_panic'\n"
            "- Input: 'I'm feeling really stressed about exams.' -> Class: 'conversational', Domain: 'none'\n\n"
            "OUTPUT FORMAT:\n"
            "Provide a JSON object with these three fields:\n"
            "- \"classification\": \"greeting\" | \"conversational\" | \"rag_required\"\n"
            "- \"standalone_query\": \"string\"\n"
            "- \"domain\": \"cbt_assertiveness\" | \"cbt_bipolar\" | \"cbt_body_acceptance\" | \"cbt_body_image\" | \"cbt_depression\" | \"cbt_eating_disorder\" | \"cbt_gad\" | \"cbt_panic\" | \"cbt_self_esteem\" | \"cbt_social_anxiety\" | \"platform\" | \"none\""
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}")
        ])
        
        self.chain = (self.prompt | self.classifier_llm | StrOutputParser()).with_config({"run_name": "RouterChain"})

    async def process_query(self, message: str, chat_history: list = [], history_summary: Optional[str] = None) -> Tuple[Literal["greeting", "conversational", "rag_required"], str, str]:
        """
        Classifies the message, generates a standalone query, and identifies the clinical domain in a single LLM call.
        Returns: (classification, standalone_query, domain)
        """
        try:
            # Prepare inputs with history summary if available
            inputs = {"input": message, "chat_history": chat_history}
            
            result = await self.chain.ainvoke(
                inputs
            )
            
            # Clean up result in case model adds markdown formatting
            clean_result = result.strip()
            if clean_result.startswith("```json"):
                clean_result = clean_result.replace("```json", "").replace("```", "").strip()
            
            data = json.loads(clean_result)
            classification = data.get("classification", "conversational").lower()
            standalone_query = data.get("standalone_query", message)
            domain = data.get("domain", "none").lower()
            
            valid_classes = ["greeting", "conversational", "rag_required"]
            valid_domains = {
                "cbt_assertiveness", "cbt_bipolar", "cbt_body_acceptance", "cbt_body_image",
                "cbt_depression", "cbt_eating_disorder", "cbt_gad", "cbt_panic",
                "cbt_self_esteem", "cbt_social_anxiety", "platform", "none"
            }
            
            final_class = classification if classification in valid_classes else "conversational"
            final_domain = domain if domain in valid_domains else "none"
            
            return final_class, standalone_query, final_domain
            
        except Exception as e:
            logger.error(f"Router/Rephraser Error: {e}")
            # Default to conversational, original message, and "none" domain on error
            return "conversational", message, "none"
