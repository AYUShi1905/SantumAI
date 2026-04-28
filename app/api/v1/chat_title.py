from fastapi import APIRouter, HTTPException
from services.summarizer import SummarizationService
from models.request import SummarizeRequest
from models.response import TitleResponse
import logging

router = APIRouter(prefix="/chat/title", tags=["chat"])

logger = logging.getLogger(__name__)

@router.post("", response_model=TitleResponse)
async def generate_chat_title(request: SummarizeRequest):
    """
    Endpoint to generate a short, descriptive title for a chat history.
    """
    try:
        if not request.chat_history:
            raise HTTPException(status_code=400, detail="Chat history cannot be empty.")
            
        summarizer = SummarizationService()
        title = await summarizer.generate_title(chat_history=request.chat_history)
        
        return TitleResponse(title=title)
        
    except Exception as e:
        logger.error(f"Error during title generation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Title generation failed: {str(e)}")
