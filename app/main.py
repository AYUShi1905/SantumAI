from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from core.exceptions import SantumException
from api.v1.ingest import router as ingest_router
from api.v1.summarize import router as summarize_router
from api.v1.chat import router as chat_router
from api.v1.chat_title import router as chat_title_router
from utils.logger import setup_logging
import logging

# Initialize Logging
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG,
    version="1.0.0"
)

# Global Exception Handlers
@app.exception_handler(SantumException)
async def santum_exception_handler(request: Request, exc: SantumException):
    """Handles all custom Santum AI exceptions."""
    logger.error(f"Santum AI Error: {exc.message} | Detail: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.message,
            "detail": exc.detail
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Catch-all for any unhandled exceptions."""
    logger.error(f"Unhandled System Error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "An internal server error occurred.",
            "detail": str(exc) if settings.DEBUG else "Please contact support if the issue persists."
        }
    )

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(ingest_router, prefix="/api/v1")
app.include_router(summarize_router, prefix="/api/v1")
app.include_router(chat_router, prefix="/api/v1")
app.include_router(chat_title_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to Santum AI RAG Service API"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)
