from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from models.request import ChatRequest
from services.llm_provider import LLMProviderService
from services.rag_service import RAGService
from utils.tokens import count_tokens
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import logging
import json

router = APIRouter(prefix="/chat", tags=["chat"])
logger = logging.getLogger(__name__)
llm_service = LLMProviderService()
rag_service = RAGService()

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
    Includes an Abuse Detection Layer (Moderation) to filter unsafe content.
    """
    try:
        # 1. Moderation Check (Abuse Detection Layer)
        is_safe, category = await moderation_service.check_message(request.message)
        
        if not is_safe:
            logger.warning(f"Moderation Filter Triggered: Category {category}")
            
            async def safety_generator():
                yield SAFETY_REFUSAL_MESSAGE
                metadata = {
                    "total_tokens": 0,
                    "status": "safety_violation",
                    "category": category
                }
                yield f"\n\n{json.dumps(metadata)}"
            
            return StreamingResponse(safety_generator(), media_type="text/event-stream")

        # 2. Convert history
        history = _convert_history(request.chat_history)
        
        # Get streaming generator from RAG service
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

        return StreamingResponse(generator, media_type="text/event-stream")

    except Exception as e:
        logger.error(f"Error in RAG chat stream: {str(e)}")
        raise HTTPException(status_code=500, detail=f"RAG Error: {str(e)}")
