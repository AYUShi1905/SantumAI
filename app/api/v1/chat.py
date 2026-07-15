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

    # 0. Validate Input Word Count based on Plan
    word_count = len(request.message.split())
    limits = {
        "free": 80,
        "standard": 100,
        "premium": 120
    }
    limit = limits.get(request.plan_level.value, 80)
    
    if word_count > limit:
        logger.warning(f"Input limit exceeded: {word_count} words (Limit: {limit} for {request.plan_level})")
        raise HTTPException(
            status_code=400, 
            detail=f"Your message is {word_count} words long, which exceeds the {limit}-word limit for the {request.plan_level.title()} plan. Please shorten your message or upgrade your plan."
        )
    
    # 1. Convert history - Only keep the last 6 messages (3 exchanges)
    # This aligns with the "Recent Context" strategy in AI Architecture Summary 2.pdf
    recent_history = request.chat_history[-6:] if len(request.chat_history) > 6 else request.chat_history
    history = _convert_history(recent_history)
    
    # 2. Get streaming generator from RAG service
    generator = rag_service.get_streaming_response(
        query=request.message,
        chat_history=history,
        plan_level=request.plan_level,

        history_summary=request.history_summary,
        remaining_tokens=request.remaining_tokens,
        happiness=request.happiness,
        stress=request.stress,
        energy=request.energy
    )

    return StreamingResponse(generator, media_type="text/event-stream")
