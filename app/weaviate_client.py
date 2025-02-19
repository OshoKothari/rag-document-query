import weaviate

client = weaviate.Client("http://localhost:8080")

def store_document(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        document_text = file.read()

    # Create schema for 'Document' class if not exists
    schema = {
        "class": "Document",
        "properties": [
            {"name": "text", "dataType": ["text"]},
        ],
    }
    client.schema.create_class(schema)

    # Store the document; Weaviate will handle vectorization automatically
    document = {
        "text": document_text,
    }
    client.data_object.create(document, class_name="Document")
    print(f"Document '{file_path}' stored in Weaviate successfully!")
