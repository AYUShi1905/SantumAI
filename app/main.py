from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from api.v1.ingest import router as ingest_router
from api.v1.summarize import router as summarize_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG,
    version="1.0.0"
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
