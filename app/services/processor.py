import fitz  # PyMuPDF
import docx
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.document import Document as DocxDocument
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List, Iterator, Union
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

    def _iter_block_items(self, parent: Union[DocxDocument, Table]) -> Iterator[Union[Paragraph, Table]]:
        """
        Yield each paragraph and table child within `parent`, in document order.
        Each returned value is an instance of either Table or Paragraph.
        """
        if isinstance(parent, DocxDocument):
            parent_elm = parent.element.body
        elif isinstance(parent, Table):
            parent_elm = parent._element
        else:
            raise TypeError("Parent must be a Document or Table object")

        for child in parent_elm.iterchildren():
            if isinstance(child, docx.oxml.text.paragraph.CT_P):
                yield Paragraph(child, parent)
            elif isinstance(child, docx.oxml.table.CT_Tbl):
                yield Table(child, parent)

    def _table_to_markdown(self, table: Table) -> str:
        """
        Converts a docx Table to a Markdown string.
        Optimized for RAG: repeats text in merged cells and sanitizes content.
        """
        markdown_rows = []
        
        # Get dimensions of the table
        rows = table.rows
        if not rows:
            return ""
            
        # We use cell objects to handle text and merged status
        for i, row in enumerate(rows):
            clean_cells = []
            for cell in row.cells:
                # Clean text: remove newlines and pipes to avoid breaking MD structure
                # Repeating text in merged cells is default behavior of cell.text in python-docx
                text = cell.text.replace("\n", " ").replace("|", "\\|").strip()
                clean_cells.append(text)
            
            markdown_rows.append(f"| {' | '.join(clean_cells)} |")
            
            # Add separator after header row
            if i == 0:
                separator = f"| {' | '.join(['---'] * len(clean_cells))} |"
                markdown_rows.append(separator)
        
        return "\n".join(markdown_rows)

    def process_docx(self, file_content: bytes) -> str:
        """
        Extracts text from DOCX content, including tables in Markdown format,
        preserving the original document order.
        """
        doc = docx.Document(io.BytesIO(file_content))
        full_content = []

        for block in self._iter_block_items(doc):
            if isinstance(block, Paragraph):
                if block.text.strip():
                    full_content.append(block.text)
            elif isinstance(block, Table):
                table_md = self._table_to_markdown(block)
                if table_md:
                    full_content.append(f"\n{table_md}\n")

        return "\n".join(full_content)

    def process_file(
        self, 
        file_content: bytes, 
        filename: str, 
        header_margin: float = 0.1, 
        footer_margin: float = 0.1,
        is_cbt_manual: bool = False
    ) -> List[Document]:
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
            metadata={
                "source": filename,
                "is_cbt_manual": is_cbt_manual
            }
        )

        # Split into chunks
        return self.text_splitter.split_documents([base_doc])
