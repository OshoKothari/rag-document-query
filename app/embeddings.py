import weaviate

def generate_embedding(text):
    """Generate embedding using Weaviate's built-in 'text2vec-contextionary' model."""
    client = weaviate.Client("http://localhost:8080")  # Adjust Weaviate URL if needed

    try:
        # Check if the 'Document' class already exists
        classes = client.schema.get()  # Corrected method
        class_names = [cls["class"] for cls in classes["classes"]]

        if "Document" not in class_names:
            # Create schema for 'Document' class if not exists
            schema = {
                "class": "Document",
                "vectorizer": "text2vec-contextionary",  # Set vectorizer to generate embeddings
                "properties": [
                    {"name": "text", "dataType": ["text"]},
                    {"name": "filename", "dataType": ["text"]},
                    {"name": "filetype", "dataType": ["text"]},
                ],
            }
            client.schema.create_class(schema)
            print("Class 'Document' created successfully!")

        # Create the document object and store it in Weaviate
        document = {
            "text": text,
            "filename": "your_filename.pdf",  # Add filename if needed
            "filetype": "pdf",  # Set file type
        }
        # Weaviate automatically generates the embedding vector upon storing the document
        client.data_object.create(document, class_name="Document")
        print(f"Document stored successfully!")

    except Exception as e:
        print(f"Error storing document and generating embedding: {e}")
