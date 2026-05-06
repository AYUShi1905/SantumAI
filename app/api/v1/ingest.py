from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks
from services.processor import DocumentProcessorService
from services.vector_db import VectorDBService
from models.response import IngestResponse
from core.exceptions import IngestionError, SantumException
from typing import Optional
import logging

router = APIRouter(prefix="/ingest", tags=["ingestion"])

logger = logging.getLogger(__name__)

@router.post("/file", response_model=IngestResponse)
async def ingest_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    header_margin: Optional[float] = Form(0.1),
    footer_margin: Optional[float] = Form(0.1),
    is_cbt_manual: bool = Form(False)
):
    """
    Endpoint to upload a PDF or DOCX, process its content, and store it in the vector database.
    """
    allowed_extensions = (".pdf", ".docx")
    if not file.filename.lower().endswith(allowed_extensions):
        raise IngestionError(
            message=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
        )

    try:
        # 1. Read file content
        content = await file.read()
        
        # 2. Process/Chunk File
        processor = DocumentProcessorService()
        try:
            documents = processor.process_file(
                content, 
                file.filename,
                header_margin=header_margin,
                footer_margin=footer_margin,
                is_cbt_manual=is_cbt_manual
            )
        except ValueError as ve:
            if str(ve) == "SCANNED_PDF":
                raise IngestionError(
                    message="The uploaded PDF appears to be a scanned document (image-based). Please upload a text-based PDF or a DOCX file."
                )
            raise IngestionError(message=str(ve))
        
        if not documents:
            raise IngestionError(message="File content could not be extracted or is empty.")

        # 3. Add to Vector DB (Background Task)
        vector_db = VectorDBService()
        background_tasks.add_task(vector_db.add_documents, documents)

        return IngestResponse(
            message="File accepted for processing. Ingestion is running in the background.",
            filename=file.filename,
            chunks_processed=len(documents)
        )
    finally:
        await file.close()

@router.get("/files")
async def get_files():
    """Returns a list of all unique files that have been ingested."""
    vector_db = VectorDBService()
    files = vector_db.list_ingested_files()
    return {"files": files, "count": len(files)}

@router.delete("/file")
async def delete_file(filename: str):
    """Deletes all data associated with a specific filename."""
    vector_db = VectorDBService()
    vector_db.delete_by_filename(filename)
    return {"message": f"Successfully deleted data for file: {filename}"}

@router.delete("/all")
async def delete_all():
    """Clears the entire collection."""
    vector_db = VectorDBService()
    vector_db.clear_collection()
    return {"message": "Successfully cleared the entire collection"}

