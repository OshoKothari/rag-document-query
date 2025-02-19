# api.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import weaviate

# Initialize Weaviate client
client = weaviate.Client("http://localhost:8080")  # Adjust Weaviate URL if needed

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/query/")
async def query_document(query_request: QueryRequest):
    """API endpoint to query the document stored in Weaviate."""
    try:
        # Perform the query against Weaviate
        result = client.query.get("Document", ["text"]).with_additional(["vector"]).with_near_text({"concepts": [query_request.query]}).do()
        
        if not result["data"]["Get"]["Document"]:
            raise HTTPException(status_code=404, detail="No relevant document found")
        
        # Extract the most relevant snippet from the retrieved document
        best_match = result["data"]["Get"]["Document"][0]
        return {"answer": best_match["text"], "document_id": best_match["id"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

