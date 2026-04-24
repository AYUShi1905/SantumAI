from fastapi import APIRouter, HTTPException
from services.summarizer import SummarizationService
from models.request import SummarizeRequest
from models.response import SummarizeResponse
import logging

router = APIRouter(prefix="/summarize", tags=["summarization"])

logger = logging.getLogger(__name__)

@router.post("", response_model=SummarizeResponse)
async def summarize_chat(request: SummarizeRequest):
    """
    Endpoint to summarize a chat history.
    """
    try:
        if not request.chat_history:
            raise HTTPException(status_code=400, detail="Chat history cannot be empty.")
            
        summarizer = SummarizationService()
        summary = await summarizer.summarize(
            chat_history=request.chat_history, 
            existing_summary=request.existing_summary
        )
        
        return SummarizeResponse(summary=summary)
        
    except Exception as e:
        logger.error(f"Error during summarization: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Summarization failed: {str(e)}")
