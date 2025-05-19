import json
from langchain.schema import Document

def load_chunks_as_documents(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    documents = []
    for chunk in chunks:
        content = chunk.get("text") or json.dumps(chunk.get("data"))
        doc = Document(page_content=content, metadata={"type": chunk.get("type", "unknown")})
        documents.append(doc)

    return documents

# Usage
documents = load_chunks_as_documents("intermediate_output.json")
