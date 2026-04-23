import fitz  # PyMuPDF
import docx
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List
import io

class DocumentProcessorService:
    """
    Service for parsing PDFs and DOCX files and chunking text for RAG ingestion.
    """

    def __init__(self, chunk_size: int = 600, chunk_overlap: int = 60):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            is_separator_regex=False,
        )

    def process_pdf(self, file_content: bytes, header_margin: float = 0.1, footer_margin: float = 0.1) -> str:
        """Extracts text from PDF content within a safe zone (ignoring headers/footers)."""
        doc = fitz.open(stream=file_content, filetype="pdf")
        text = ""
        page_count = len(doc)
        
        for page in doc:
            # Get page dimensions
            rect = page.rect
            width = rect.width
            height = rect.height
            
            # Define safe zone (clipping rectangle)
            # x0, y0, x1, y1
            safe_rect = fitz.Rect(
                0, 
                height * header_margin, 
                width, 
                height * (1.0 - footer_margin)
            )
            
            # Extract text only from the safe zone
            text += page.get_text("text", clip=safe_rect)
            
        doc.close()

        if page_count > 0 and not text.strip():
            raise ValueError("SCANNED_PDF")
            
        return text

    def process_docx(self, file_content: bytes) -> str:
        """Extracts text from DOCX content (paragraphs only)."""
        doc = docx.Document(io.BytesIO(file_content))
        return "\n".join([para.text for para in doc.paragraphs])

    def process_file(self, file_content: bytes, filename: str, header_margin: float = 0.1, footer_margin: float = 0.1) -> List[Document]:
        """
        Parses file content based on extension and returns chunked Documents.
        """
        if filename.lower().endswith(".pdf"):
            full_text = self.process_pdf(file_content, header_margin, footer_margin)
        elif filename.lower().endswith(".docx"):
            full_text = self.process_docx(file_content)
        else:
            raise ValueError(f"Unsupported file extension: {filename}")
        
        if not full_text.strip():
            return []

        # Create initial document
        base_doc = Document(
            page_content=full_text,
            metadata={"source": filename}
        )

        # Split into chunks
        return self.text_splitter.split_documents([base_doc])
