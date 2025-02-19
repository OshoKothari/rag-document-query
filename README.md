Sure! Here's the updated **README.md** based on your requirements:

---

# Retrieval Augmented Generation (RAG) System

This project implements a Retrieval Augmented Generation (RAG) system using Weaviate as the vector database and Google Gemini API for generating answers based on document content. The system allows users to upload various types of documents (PDF, DOCX, TXT, JSON), query those documents, and receive relevant answers. Additionally, it supports JSON aggregation for enhanced data analysis and summarization.

## Features

- **Document Upload**: Upload documents of various types, including PDF, DOCX, TXT, and JSON.
- **Document Storage**: Uploaded documents are processed and stored in Weaviate, a powerful vector database.
- **Question Answering**: Users can ask questions about the content of the documents, and the system retrieves answers based on document content using the Weaviate database and Gemini API.
- **JSON Aggregation**: The system aggregates JSON data and provides summarized answers with structured JSON responses.
- **Deployment**: The app is deployed using Vercel for continuous deployment, with the backend powered by FastAPI.

## Prerequisites

Before running this project locally or deploying it, ensure you have the following:

- Python 3.7 or higher
- Docker (for running Weaviate locally if needed)
- Git (for version control)
- A Weaviate instance running locally or remotely (you can use Weaviate Cloud or Docker to spin up an instance).
- Google Gemini API key for accessing the model (see setup instructions below).

## Setup Instructions

### 1. Clone the Repository

Clone this repository to your local machine using the following command:

```bash
git clone https://github.com/oshokothari/rag-document=query.git
cd rag-system
```

### 2. Install Dependencies

Make sure you have a virtual environment set up. If not, create one and activate it:

```bash
python -m venv venv
source venv/bin/activate  # For Mac/Linux
venv\Scripts\activate  # For Windows
```

Then, install the required Python packages:

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the project root directory and add the following environment variables:

```ini
GOOGLE_API_KEY="your_google_api_key"
WEAVIATE_URL="http://localhost:8080"  # Adjust if you are using a remote Weaviate instance
```

Replace `"your_google_api_key"` with your actual Google Gemini API key.

### 4. Run the Application Locally

If you have Docker installed, you can start Weaviate using Docker Compose by running the following command:

```bash
docker-compose up --build
```

This will spin up the Weaviate instance locally.

Once Weaviate is up and running, you can start the FastAPI app using Uvicorn:

```bash
uvicorn app.main:app --reload
```

The app will be running locally at `http://127.0.0.1:8000`. You can now visit the app in your browser.

### 5. Testing the System

1. **Upload Documents**: Use the `/upload` endpoint to upload documents. You can upload PDF, DOCX, TXT, or JSON files.
2. **Ask Questions**: Use the `/query` endpoint to ask questions related to the uploaded documents. The system will return relevant answers based on the document content.
3. **JSON Aggregation**: If you upload a JSON document, the system will aggregate its data and provide a summarized response.
