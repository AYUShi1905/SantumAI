from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from models.request import ChatRequest
from services.llm_provider import LLMProviderService
from services.rag_service import RAGService
from utils.tokens import count_tokens
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import logging
import json
from services.moderation import ModerationService
import time 

router = APIRouter(prefix="/chat", tags=["chat"])
logger = logging.getLogger(__name__)
llm_service = LLMProviderService()
rag_service = RAGService()
moderation_service = ModerationService()

def _convert_history(chat_history):
    """Helper to convert ChatMessage models to LangChain messages."""
    messages = []
    for msg in chat_history:
        if msg.role == "human":
            messages.append(HumanMessage(content=msg.content))
        elif msg.role == "ai":
            messages.append(AIMessage(content=msg.content))
    return messages

@router.post("/stream")
async def chat_rag_stream(request: ChatRequest):
    """
    PRODUCTION RAG ENDPOINT:
    Streams a response grounded in counseling manuals retrieved from Qdrant.
    Parallelized orchestration (Moderation, Routing, Retrieval) handled in RAGService.
    """
    start_time = time.time()
    
    # 1. Convert history
    history = _convert_history(request.chat_history)
    
    # 2. Get streaming generator from RAG service
    generator = rag_service.get_streaming_response(
        query=request.message,
        chat_history=history,
        plan_level=request.plan_level,
        use_reasoning=request.use_reasoning,
        history_summary=request.history_summary,
        remaining_tokens=request.remaining_tokens,
        happiness=request.happiness,
        stress=request.stress,
        energy=request.energy
    )

    async def ttft_logging_wrapper():
        first_token_sent = False
        async for chunk in generator:
            if not first_token_sent and chunk:
                ttft = time.time() - start_time
                logger.info(f"BACKEND_TTFT: {ttft:.4f}s | Query: {request.message[:50]}...")
                first_token_sent = True
            yield chunk

    return StreamingResponse(ttft_logging_wrapper(), media_type="text/event-stream")
