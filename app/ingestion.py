import os
import uuid
import json
import PyPDF2
import docx
from app.weaviate_client import client
from app.embeddings import generate_embedding

def generate_session_id():
    """Generate a unique session ID (UUID) for each uploaded document."""
    return str(uuid.uuid4())

def chunk_pdf(file_path):
    """Chunk the PDF into smaller sections (pages or paragraphs)."""
    with open(file_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        chunks = []
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                chunks.extend(text.split('\n'))  # Splitting by line
        return chunks

def chunk_docx(file_path):
    """Chunk DOCX files into paragraphs."""
    doc = docx.Document(file_path)
    return [para.text for para in doc.paragraphs if para.text.strip()]

def chunk_txt(file_path):
    """Chunk TXT files into lines."""
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file.readlines() if line.strip()]

def chunk_json(file_path):
    """Extract JSON data as a single chunk."""
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        return [json.dumps(data)]  # Store as a single JSON string

def store_document_in_weaviate(file_path, file_type, session_id):
    """Extract, chunk, generate embeddings, and store in Weaviate."""
    try:
        chunks = []
        if file_type == 'pdf':
            chunks = chunk_pdf(file_path)
        elif file_type == 'docx':
            chunks = chunk_docx(file_path)
        elif file_type == 'txt':
            chunks = chunk_txt(file_path)
        elif file_type == 'json':
            chunks = chunk_json(file_path)

        for idx, chunk in enumerate(chunks):
            text = chunk.strip()
            if not text:
                continue  # Skip empty chunks

            embedding = generate_embedding(text)

            data_object = {
                "text": text,
                "filename": os.path.basename(file_path),
                "filetype": file_type,
                "chunk_id": f"{session_id}_{idx}",
                "session_id": session_id  
            }

            client.data_object.create(data_object, class_name="Document", vector=embedding)
            print(f"Chunk {idx} stored successfully!")

    except Exception as e:
        print(f"Error storing document in Weaviate: {e}")
