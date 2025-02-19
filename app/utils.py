from PyPDF2 import PdfReader
from docx import Document as DocxDocument
import os

def extract_text(file_path, file_type):
    """Extract text from different file types."""
    if file_type == "pdf":
        return extract_text_from_pdf(file_path)
    elif file_type == "docx":
        return extract_text_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

def extract_text_from_pdf(file_path):
    """Extract text from PDF."""
    try:
        with open(file_path, 'rb') as f:
            reader = PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {e}")

def extract_text_from_docx(file_path):
    """Extract text from DOCX."""
    try:
        doc = DocxDocument(file_path)
        text = ""
        for para in doc.paragraphs:
            text += para.text
        return text
    except Exception as e:
        raise Exception(f"Error extracting text from DOCX: {e}")
