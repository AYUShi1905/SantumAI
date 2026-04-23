from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from models.request import ChatRequest
from services.llm_provider import LLMProviderService
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import logging
import json

router = APIRouter(prefix="/chat", tags=["chat"])
logger = logging.getLogger(__name__)
llm_service = LLMProviderService()

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
        
        # Add history
        for msg in request.chat_history:
            if msg.role == "human":
                messages.append(HumanMessage(content=msg.content))
            elif msg.role == "ai":
                messages.append(AIMessage(content=msg.content))
        
        # Add current message
        messages.append(HumanMessage(content=request.message))

        async def generate():
            total_tokens = 0
            async for chunk in llm.astream(messages):
                if chunk.content:
                    yield chunk.content
                    # Rough token estimation for test
                    total_tokens += len(chunk.content.split()) * 1.3
            
            # Final metadata chunk
            metadata = {
                "total_tokens": int(total_tokens),
                "status": "completed",
                "mode": "test_no_rag"
            }
            yield f"\n\n{json.dumps(metadata)}"

        return StreamingResponse(generate(), media_type="text/event-stream")

    except Exception as e:
        logger.error(f"Error in test chat stream: {str(e)}")
        raise HTTPException(status_code=500, detail=f"LLM Error: {str(e)}")
