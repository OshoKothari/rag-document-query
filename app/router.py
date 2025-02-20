from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel
import os
import weaviate
import uuid
import json
import google.generativeai as genai
from app.ingestion import store_document_in_weaviate

router = APIRouter()
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize Weaviate client
client = weaviate.Client("http://localhost:8080")

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY", "AIzaSyAbinpYZm51dpu1D4k9kM9ceOpBctwhLdw"))
model = genai.GenerativeModel('gemini-pro')

class QueryRequest(BaseModel):
    question: str
    session_id: str  

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """Upload document and store in Weaviate."""
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

        file_type = file.filename.split(".")[-1].lower()
        session_id = str(uuid.uuid4())

        store_document_in_weaviate(file_path, file_type, session_id)

        return {"message": f"File '{file.filename}' uploaded successfully!", "session_id": session_id}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload error: {str(e)}")

@router.post("/query/")
async def query_document(query: QueryRequest):
    """Query Weaviate for answers related to a specific session."""
    try:
        response = client.query.get("Document", ["text"]).with_near_text({
            "concepts": [query.question]
        }).with_where({
            "path": ["session_id"],
            "operator": "Equal",
            "valueString": query.session_id  
        }).do()

        documents = response.get("data", {}).get("Get", {}).get("Document", [])
        
        if not documents:
            return {"answer": "No relevant information found."}

        document_text = " ".join([doc["text"] for doc in documents])

        # Generate final answer using Gemini
        gemini_response = model.generate_content(f"Answer the following query based on the document:\n{query.question}\nDocument: {document_text}").text

        return {"answer": gemini_response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query error: {str(e)}")

@router.post("/aggregate-json/")
async def aggregate_json(session_id: str):
    """Aggregate JSON data for a specific session."""
    try:
        response = client.query.get("Document", ["text"]).with_where({
            "path": ["session_id"],
            "operator": "Equal",
            "valueString": session_id  
        }).do()

        documents = response.get("data", {}).get("Get", {}).get("Document", [])

        if not documents:
            return {"aggregated_data": "No JSON documents found for this session."}

        json_data = [json.loads(doc["text"]) for doc in documents if doc["text"]]

        # Merge all JSON data
        aggregated_json = {}
        for entry in json_data:
            for key, value in entry.items():
                if key in aggregated_json:
                    if isinstance(aggregated_json[key], list) and isinstance(value, list):
                        aggregated_json[key].extend(value)
                    elif isinstance(aggregated_json[key], dict) and isinstance(value, dict):
                        aggregated_json[key].update(value)
                else:
                    aggregated_json[key] = value

        # Generate summary with Gemini
        gemini_response = model.generate_content(f"Summarize the following JSON data:\n{json.dumps(aggregated_json, indent=2)}").text

        return {"aggregated_json": aggregated_json, "summary": gemini_response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Aggregation error: {str(e)}")
