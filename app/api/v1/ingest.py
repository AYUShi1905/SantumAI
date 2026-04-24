from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from services.processor import DocumentProcessorService
from services.vector_db import VectorDBService
from models.response import IngestResponse
from typing import Optional
import logging

router = APIRouter(prefix="/ingest", tags=["ingestion"])

logger = logging.getLogger(__name__)

@router.post("/file", response_model=IngestResponse)
async def ingest_file(
    file: UploadFile = File(...),
    header_margin: Optional[float] = Form(0.1),
    footer_margin: Optional[float] = Form(0.1),
    is_cbt_manual: bool = Form(False)
):
    """
    Endpoint to upload a PDF or DOCX, process its content, and store it in the vector database.
    
    Args:
        file: The PDF or DOCX file to ingest.
        header_margin: Percentage (0.0 - 0.2) of the top of the PDF to ignore (default 0.1).
        footer_margin: Percentage (0.0 - 0.2) of the bottom of the PDF to ignore (default 0.1).
        is_cbt_manual: Whether this document is a CBT manual (restricted to Premium users).
    """
    allowed_extensions = (".pdf", ".docx")
    if not file.filename.lower().endswith(allowed_extensions):
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
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
                raise HTTPException(
                    status_code=400, 
                    detail="The uploaded PDF appears to be a scanned document (image-based). Please upload a text-based PDF or a DOCX file."
                )
            raise HTTPException(status_code=400, detail=str(ve))
        
        if not documents:
            raise HTTPException(status_code=400, detail="File content could not be extracted or is empty.")

        # 3. Add to Vector DB
        vector_db = VectorDBService()
        vector_db.add_documents(documents)

        return IngestResponse(
            message="File successfully processed and ingested",
            filename=file.filename,
            chunks_processed=len(documents)
        )

    except Exception as e:
        logger.error(f"Error during ingestion: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")
    finally:
        await file.close()

@router.get("/files")
async def get_files():
    """Returns a list of all unique files that have been ingested."""
    try:
        vector_db = VectorDBService()
        files = vector_db.list_ingested_files()
        return {"files": files, "count": len(files)}
    except Exception as e:
        logger.error(f"Error listing files: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/file")
async def delete_file(filename: str):
    """Deletes all data associated with a specific filename."""
    try:
        vector_db = VectorDBService()
        vector_db.delete_by_filename(filename)
        return {"message": f"Successfully deleted data for file: {filename}"}
    except Exception as e:
        logger.error(f"Error deleting file {filename}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/all")
async def delete_all():
    """Clears the entire collection."""
    try:
        vector_db = VectorDBService()
        vector_db.clear_collection()
        return {"message": "Successfully cleared the entire collection"}
    except Exception as e:
        logger.error(f"Error clearing collection: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

