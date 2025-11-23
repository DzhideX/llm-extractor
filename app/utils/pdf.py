import fitz
from typing import Dict


class PDFParser:
    """Utility class for parsing PDF documents"""
    
    def __init__(self, pdf_path: str):
        """
        Initialize PDF parser.
        
        Args:
            pdf_path: Path to PDF file
        """
        self.pdf_path = pdf_path
        self.doc = fitz.open(pdf_path)
    
    def extract_full_text(self) -> str:
        """
        Extract all text from PDF with page markers.
        
        Returns:
            str: Full text with '--- PAGE X ---' markers between pages
        """
        full_text = ""
        for page_num in range(len(self.doc)):
            page = self.doc[page_num]
            page_number = page_num + 1

            # Here we add a marker to the text to indicate the start of a new page.
            # This is useful for the LLM to understand the structure of the document
            # and positioning of each clause relative to the page.
            page_marker = f"\n\n--- PAGE {page_number} ---\n\n"
            full_text += page_marker + page.get_text()
        return full_text
    
    def get_metadata(self) -> dict:
        """
        Extract PDF metadata.
        
        Returns:
            dict: PDF metadata (title, author, etc.)
        """
        return self.doc.metadata
    
    def get_page_count(self) -> int:
        """
        Get total number of pages.
        
        Returns:
            int: Total page count
        """
        return len(self.doc)
    
    def close(self):
        """
        Close the PDF document and release resources.
        """
        self.doc.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


def extract_pdf_text(pdf_path: str) -> Dict[str, any]:
    """
    Extract text and metadata from a PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        
    Raises:
        Exception: If PDF cannot be opened or parsed
        
    Returns:
        dict: Contains 'full_text', 'page_count', and 'metadata' keys
    """
    with PDFParser(pdf_path) as parser:
        return {
            'full_text': parser.extract_full_text(),
            'page_count': parser.get_page_count(),
            'metadata': parser.get_metadata()
        }