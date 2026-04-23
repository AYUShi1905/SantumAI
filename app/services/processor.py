import fitz  # PyMuPDF
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List
import io

class DocumentProcessorService:
    """
    Service for parsing PDFs and chunking text for RAG ingestion.
    """

    def __init__(self, chunk_size: int = 600, chunk_overlap: int = 60):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            is_separator_regex=False,
        )

    def process_pdf(self, file_content: bytes, filename: str) -> List[Document]:
        """
        Parses PDF content and returns a list of chunked LangChain Documents.
        """
        doc = fitz.open(stream=file_content, filetype="pdf")
        full_text = ""
        
        for page in doc:
            full_text += page.get_text()
            
        doc.close()

        # Create initial document
        base_doc = Document(
            page_content=full_text,
            metadata={"source": filename}
        )

        # Split into chunks
        return self.text_splitter.split_documents([base_doc])
