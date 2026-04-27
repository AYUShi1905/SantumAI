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

@router.post("/test-stream")
async def chat_test_stream(request: ChatRequest):
    """
    SIMPLE TEST ENDPOINT:
    Streams a direct response from the LLM (bypasses RAG).
    Used to verify Groq/LLM integration.
    """
    try:
        llm = llm_service.get_llm(use_reasoning=request.use_reasoning)
        
        # Prepare messages
        messages = [
            SystemMessage(content="You are a helpful and empathetic AI counselor.")
        ]
        
        # Add summary if provided
        if request.history_summary:
            messages.append(SystemMessage(content=f"Summary of previous conversation: {request.history_summary}"))
        
        # Add history
        messages.extend(_convert_history(request.chat_history))
        
        # Add current message
        messages.append(HumanMessage(content=request.message))

        async def generate():
            full_response = ""
            async for chunk in llm.astream(messages):
                if chunk.content:
                    full_response += chunk.content
                    yield chunk.content
            
            # Final metadata chunk
            metadata = {
                "total_tokens": count_tokens(full_response),
                "status": "completed",
                "mode": "test_no_rag"
            }
            yield f"\n\n{json.dumps(metadata)}"

        return StreamingResponse(generate(), media_type="text/event-stream")

    except Exception as e:
        logger.error(f"Error in test chat stream: {str(e)}")
        raise HTTPException(status_code=500, detail=f"LLM Error: {str(e)}")

@router.post("/stream")
async def chat_rag_stream(request: ChatRequest):
    """
    PRODUCTION RAG ENDPOINT:
    Streams a response grounded in counseling manuals retrieved from Qdrant.
    """
    try:
        # Convert history
        history = _convert_history(request.chat_history)
        
        # Get streaming generator from RAG service
        generator = rag_service.get_streaming_response(
            query=request.message,
            chat_history=history,
            plan_level=request.plan_level,
            use_reasoning=request.use_reasoning,
            history_summary=request.history_summary,
            remaining_tokens=request.remaining_tokens
        )

        return StreamingResponse(generator, media_type="text/event-stream")

    except Exception as e:
        logger.error(f"Error in RAG chat stream: {str(e)}")
        raise HTTPException(status_code=500, detail=f"RAG Error: {str(e)}")
