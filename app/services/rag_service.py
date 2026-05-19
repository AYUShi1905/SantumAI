import asyncio
import re
import random
from typing import AsyncGenerator, List, Dict, Any, Optional
import json
import logging
from langchain_classic.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import BaseMessage

from qdrant_client.http import models as rest
from services.llm_provider import LLMProviderService
from services.vector_db import VectorDBService
from services.router import RouterService
from services.moderation import ModerationService
from services.prompt_builder import SystemPromptBuilder
from models.request import PlanLevel
from utils.tokens import count_tokens

# Initialize Logger
logger = logging.getLogger(__name__)

# Heuristic patterns for pure greetings
GREETING_PATTERNS = [
    r"^(hi|hello|hey|yo|hi there|hello there)(\!|\.|\?)*$",
    r"^(good\s+(morning|afternoon|evening))(\!|\.|\?)*$",
    r"^(is\s+anyone\s+(there|around))(\!|\.|\?)*$",
    r"^(hi|hello)\s+sai(\s+ai)?(\!|\.|\?)*$",
    r"^(hi|hello)\s+santum(\s+ai)?(\!|\.|\?)*$"
]

GREETING_RESPONSES = [
    "Hello! I'm Sai, your supportive companion. I'm here to listen and support you. How are you feeling today?",
    "Hi there! It's good to see you. I'm here whenever you're ready to talk. What's on your mind?",
    "Hello! I'm here and ready to support you in any way I can. How has your day been so far?",
    "Hi! I'm Sai. I'm here to provide a safe space for you. How can I help you today?"
]

class RAGService:
    """
    Orchestration service for the Retrieval-Augmented Generation pipeline.
    """

    def __init__(self):
        self.llm_service = LLMProviderService()
        self.vector_db_service = VectorDBService()
        self.router_service = RouterService()
        self.moderation_service = ModerationService()

    def _is_pure_greeting(self, text: str) -> bool:
        """Checks if the query is a simple greeting that can be fast-tracked."""
        normalized = text.lower().strip()
        # If more than 4 words, it likely contains emotional context or a specific query
        if len(normalized.split()) > 4:
            return False
            
        for pattern in GREETING_PATTERNS:
            if re.match(pattern, normalized):
                return True
        return False

    async def _handle_heuristic_greeting(self, plan_level: PlanLevel) -> AsyncGenerator[str, None]:
        """Streams a pre-defined empathetic greeting response."""
        response = random.choice(GREETING_RESPONSES)
        
        # Simulate slight streaming for natural feel, though nearly instant
        words = response.split()
        current_tokens = 0
        for i, word in enumerate(words):
            part = word + (" " if i < len(words) - 1 else "")
            current_tokens += count_tokens(part)
            yield part
            # No real need to sleep, but ensures it's treated as a stream
            await asyncio.sleep(0.01) 
            
        metadata = {
            "total_tokens": current_tokens,
            "status": "completed",
            "model_used": "heuristic",
            "plan": plan_level,
            "mode": "fast_track"
        }
        yield f"\n\n{json.dumps(metadata)}"

    def _get_prompts(
        self, 
        history_summary: Optional[str] = None, 
        plan_level: PlanLevel = PlanLevel.FREE, 
        happiness: float = 5.0,
        stress: float = 5.0,
        energy: float = 5.0,
        has_context: bool = True
    ) -> ChatPromptTemplate:
        """Defines the hardened system prompts using the centralized PromptBuilder."""
        
        # 1. Initialize Builder
        builder = SystemPromptBuilder(
            plan_level=plan_level,
            happiness=happiness,
            stress=stress,
            energy=energy
        )
        
        # 2. Build System Prompt String
        system_prompt_str = builder.build(has_context=has_context)
        
        # 3. Assemble LangChain Messages
        qa_messages = []
        if history_summary:
            qa_messages.append(("system", f"Summary of previous conversation: {history_summary}"))

        qa_messages.extend([
            ("system", system_prompt_str),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])
        
        return ChatPromptTemplate.from_messages(qa_messages)

    async def get_streaming_response(
        self, 
        query: str, 
        chat_history: List[BaseMessage],
        plan_level: PlanLevel = PlanLevel.FREE,
        use_reasoning: Optional[bool] = None,
        history_summary: Optional[str] = None,
        remaining_tokens: int = 0,
        happiness: float = 5.0,
        stress: float = 5.0,
        energy: float = 5.0
    ) -> AsyncGenerator[str, None]:
        """
        Generates a streaming RAG response with hardened security and token enforcement.
        Utilizes asyncio.gather for parallel orchestration (Phase 2).
        """
        # 0. Pre-check for tokens
        if remaining_tokens <= 0:
            yield "❌ You have run out of tokens. Please top up your balance to continue the conversation."
            yield f"\n\n{json.dumps({'total_tokens': 0, 'status': 'insufficient_balance'})}"
            return

        # 0.1 HEURISTIC FAST-TRACK: Bypass for pure greetings (Sub-100ms goal)
        if self._is_pure_greeting(query) and not chat_history:
            async for chunk in self._handle_heuristic_greeting(plan_level):
                yield chunk
            return

        # 1. Parallel Orchestration (Phase 2 - Optimized)
        # Fire all tasks in parallel as background tasks
        mod_task = asyncio.create_task(self.moderation_service.check_message(query))
        router_task = asyncio.create_task(self.router_service.process_query(query, chat_history, history_summary))
        
        # Define and fire retrieval task (Speculative Search)
        vectorstore = self.vector_db_service.get_vectorstore()
        search_kwargs = {"k": 5}
        if plan_level != PlanLevel.PREMIUM:
            search_kwargs["filter"] = rest.Filter(
                must=[
                    rest.FieldCondition(
                        key="metadata.is_cbt_manual",
                        match=rest.MatchValue(value=False)
                    )
                ]
            )
        retriever = vectorstore.as_retriever(search_kwargs=search_kwargs)
        retrieval_task = asyncio.create_task(retriever.ainvoke(query))

        # 2. Wait for Moderation & Routing (Usually faster than retrieval/embedding)
        try:
            # We wait for the fastest "check" components first to allow early exits
            # results = await asyncio.gather(mod_task, router_task, return_exceptions=True)
            # Unpack results
            moderation_result = await mod_task
            router_result = await router_task
        except Exception as e:
            logger.error(f"Error in parallel orchestration tasks: {e}")
            moderation_result = (True, None) # Fail-open
            router_result = ("simple", query)

        # 2.1 Safety Check (Critical Priority)
        is_safe, category = moderation_result
        if not is_safe:
            # Cancel retrieval if it's still running
            retrieval_task.cancel()
            
            current_tokens = 0
            async for chunk in self.moderation_service.create_empathetic_refusal(category, query):
                if chunk:
                    current_tokens += count_tokens(chunk)
                    yield chunk
            
            metadata = {
                "total_tokens": current_tokens,
                "status": "safety_violation",
                "category": category,
                "model_used": "moderator",
                "mode": "safety_refusal"
            }
            yield f"\n\n{json.dumps(metadata)}"
            return
        
        # 3. Reasoning & Routing Result
        classification, standalone_query = router_result
        if use_reasoning is None:
            use_reasoning = (classification == "complex")
        
        # 4. HEURISTIC: Skip retrieval ONLY for pure greetings or basic acknowledgments on first message
        # Informational queries (FAQ) are now classified as 'complex' by the router to ensure retrieval.
        skip_retrieval = (classification == "simple") and not chat_history
        
        if skip_retrieval:
            # Cancel retrieval - we don't need it for basic greetings/acknowledgments
            retrieval_task.cancel()
            
            llm = self.llm_service.get_llm(use_reasoning=use_reasoning, plan_level=plan_level)
            qa_prompt = self._get_prompts(
                history_summary=history_summary, 
                plan_level=plan_level, 
                happiness=happiness,
                stress=stress,
                energy=energy
            )
            chain = (qa_prompt | llm).with_config({"run_name": "GreetingResponseChain"})
            
            full_response = ""
            current_output_tokens = 0
            limit_reached = False

            async for chunk in chain.astream({"input": query, "chat_history": chat_history, "context": "No specific context needed for this greeting."}):
                # 1. Capture text content
                if chunk.content:
                    full_response += chunk.content
                    yield chunk.content
                
                # 2. Capture accurate Output tokens
                meta = None
                if hasattr(chunk, "usage_metadata") and chunk.usage_metadata:
                    meta = chunk.usage_metadata
                elif hasattr(chunk, "response_metadata") and chunk.response_metadata:
                    meta = chunk.response_metadata.get("token_usage")
                
                if meta:
                    current_output_tokens = meta.get("output_tokens", 0)
                    logger.info(f"GROQ_OUTPUT_METADATA (Greeting): {meta}")
            
            # Final Calculation: Sum of (User Query) + (AI Response)
            query_tokens = count_tokens(query)
            if current_output_tokens == 0:
                current_output_tokens = count_tokens(full_response)
                
            current_total_tokens = query_tokens + current_output_tokens

            metadata = {
                "total_tokens": current_total_tokens,
                "status": "completed",
                "model_used": "reasoning" if use_reasoning else "simple",
                "plan": plan_level,
                "mode": "greeting_hardened"
            }
            yield f"\n\n{json.dumps(metadata)}"
            return

        # 5. Wait for Retrieval (if not already finished)
        try:
            docs = await retrieval_task
        except Exception as e:
            logger.error(f"Retrieval Error: {e}")
            docs = []

        # 6. Final QA Generation (Phase 3)
        # We manually build the chain to ensure we get AIMessageChunks with metadata
        llm = self.llm_service.get_llm(use_reasoning=use_reasoning)
        qa_prompt = self._get_prompts(
            history_summary=history_summary, 
            plan_level=plan_level, 
            happiness=happiness,
            stress=stress,
            energy=energy,
            has_context=True
        )

        # Manually format the context from docs
        context_str = "\n\n".join([doc.page_content for doc in docs])
        
        # Build the manual chain
        chain = (qa_prompt | llm).with_config({"run_name": "MainRAGChain"})

        full_response = ""
        current_output_tokens = 0
        limit_reached = False

        async for chunk in chain.astream(
            {"input": query, "chat_history": chat_history, "context": context_str}
        ):
            # 1. Capture text content
            if chunk.content:
                full_response += chunk.content
                yield chunk.content

            # 2. Capture accurate Output tokens only (to ignore RAG DATA overhead)
            meta = None
            if hasattr(chunk, "usage_metadata") and chunk.usage_metadata:
                meta = chunk.usage_metadata
            elif hasattr(chunk, "response_metadata") and chunk.response_metadata:
                meta = chunk.response_metadata.get("token_usage")
            
            if meta:
                current_output_tokens = meta.get("output_tokens", 0)
                logger.info(f"GROQ_OUTPUT_METADATA: {meta}")

        # Final Calculation: Sum of (User Query) + (AI Response)
        # This explicitly ignores RAG Data, System Prompt, and History overhead.
        query_tokens = count_tokens(query)
        # Fallback for output tokens if metadata failed
        if current_output_tokens == 0:
            current_output_tokens = count_tokens(full_response)
            
        current_total_tokens = query_tokens + current_output_tokens

        # Final metadata chunk
        metadata = {
            "total_tokens": current_total_tokens,
            "status": "completed",
            "model_used": "reasoning" if use_reasoning else "simple",
            "plan": plan_level,
            "mode": "rag_complex"
        }
        yield f"\n\n{json.dumps(metadata)}"
