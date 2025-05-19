import json

def create_chunks_from_json(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        items = json.load(f)

    chunks = []
    for item in items:
        if item["type"] == "table":
            chunks.append({
                "type": "table",
                "data": item["data"]
            })
        else:
            chunks.append({
                "type": item["type"],
                "data": item["text"]
            })

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    return chunks

# --- Usage ---
if __name__ == "__main__":
    create_chunks_from_json("intermediate_output.json", "doc_chunks.json")
