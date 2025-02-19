import weaviate

def recreate_document_class():
    client = weaviate.Client("http://localhost:8080")  # Adjust Weaviate URL if needed

    # Delete the existing Document class
    try:
        client.schema.delete_class("Document")
        print("Deleted existing Document class.")
    except Exception as e:
        print(f"Error deleting Document class: {e}")

    # Create the Document class with the correct vectorizer
    schema = {
        "class": "Document",
        "vectorizer": "text2vec-contextionary",  # Set the correct vectorizer
        "properties": [
            {"name": "text", "dataType": ["text"]},
            {"name": "filename", "dataType": ["text"]},
            {"name": "filetype", "dataType": ["text"]},
        ]
    }

    try:
        client.schema.create_class(schema)
        print("Created Document class with correct vectorizer!")
    except Exception as e:
        print(f"Error creating Document class: {e}")

if __name__ == "__main__":
    recreate_document_class()
