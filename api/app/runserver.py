import pdfplumber
import re
import json
import chromadb
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction

# ---------- PDF Extraction and Nested Section Parsing ----------

QUOTE_PAIRS = [
    ('"', '"'), ('“', '”'), ('„', '“'), ('«', '»'), ('‹', '›'), ('‟', '”'),
    ('❝', '❞'), ('〝', '〞'), ('＂', '＂')
]

def extract_title_and_rest(text):
    text = text.strip()
    title = None
    remainder = text

    for open_q, close_q in QUOTE_PAIRS:
        pattern = re.escape(open_q) + r'(.+?)' + re.escape(close_q)
        match = re.search(pattern, text)
        if match:
            title = match.group(1).strip()
            remainder = text.replace(match.group(0), '').strip()
            return title, remainder

    if text and (text.isupper() or (text.istitle() and len(text.split()) <= 6)):
        return text, ""

    return None, remainder

section_header_re = re.compile(
    r"""^\s*
    (?P<header>
        (?:\d+(?:\.\d+)*\.)     # e.g. 1. or 1.1. or 2.6.4.
        | [a-zA-Z]\.            # e.g. a. or B.
        | \([a-zA-Z0-9]+\)      # e.g. (a), (1)
    )
    \s*
    (?P<rest>.*)?$
    """, re.VERBOSE
)

def is_top_level_section(header):
    return bool(re.match(r"^\d+\.$", header))

def split_section_numbers(header):
    h = header.rstrip('.')
    if header.startswith('(') and header.endswith(')'):
        return [header]
    if re.match(r"^[a-zA-Z]\.$", header):
        return [header]
    parts = h.split('.')
    return parts

def insert_section(root, section_numbers, section_data):
    current = root
    for i, part in enumerate(section_numbers):
        if "children" not in current:
            current["children"] = {}

        if i == 0:
            key = f"{part}_page_{section_data['page']}"
        else:
            key = part

        if key not in current["children"]:
            current["children"][key] = {
                "section_header": part + ('.' if not part.endswith('.') else ''),
                "paragraph": "",
            }
        current = current["children"][key]

        if i == len(section_numbers) - 1:
            for k, v in section_data.items():
                if k == "paragraph":
                    current[k] += (v + "\n")
                else:
                    current[k] = v

def flatten_tree(node):
    def helper(node):
        res = {}
        for k in ("page", "section_header", "topic", "section_title", "paragraph"):
            if k in node:
                if k == "paragraph":
                    res[k] = node[k].strip()
                else:
                    res[k] = node[k]
        if "children" in node:
            res["children"] = []
            for key in sorted(node["children"].keys(), key=lambda x: (len(x), x)):
                res["children"].append(helper(node["children"][key]))
        return res
    return helper(node)

def extract_sections(pdf_path):
    root = {
        "section_header": "root",
        "paragraph": "",
        "children": {}
    }

    current_section_numbers = None
    current_section_data = {}
    buffer = []

    def flush():
        nonlocal current_section_numbers, current_section_data, buffer
        if current_section_numbers:
            current_section_data["paragraph"] = "\n".join(buffer).strip()
            insert_section(root, current_section_numbers, current_section_data)
        buffer = []
        current_section_numbers = None
        current_section_data = {}

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            lines = text.split("\n")
            for line in lines:
                line = line.strip()
                match = section_header_re.match(line)
                if match:
                    flush()
                    header = match.group("header").strip()
                    rest_of_line = match.group("rest") or ""

                    current_section_numbers = split_section_numbers(header)
                    current_section_data = {
                        "page": page_num,
                        "section_header": header
                    }

                    title, rest = extract_title_and_rest(rest_of_line)
                    if title:
                        if is_top_level_section(header):
                            current_section_data["topic"] = title
                        else:
                            current_section_data["section_title"] = title
                    if rest:
                        buffer.append(rest)
                else:
                    if current_section_numbers:
                        buffer.append(line)

        flush()

    return flatten_tree(root)

# ---------- Chunk Generation ----------

def generate_chunks(node, parent_metadata=None):
    chunks = []
    parent_metadata = parent_metadata or {}

    metadata = parent_metadata.copy()
    for key in ("page", "section_title", "topic"):
        if key in node:
            metadata[key] = node[key]

    paragraph = node.get("paragraph", "").strip()
    if paragraph:
        chunks.append({
            "data": paragraph,
            "metadata": metadata
        })

    for child in node.get("children", []):
        chunks.extend(generate_chunks(child, metadata))

    return chunks

def save_to_json(data, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ---------- Main Flow ----------

if __name__ == "__main__":
    pdf_path = "your_file.pdf"  # Replace with your actual PDF path
    nested_output_path = "nested_sections.json"
    chunks_output_path = "chunks.json"

    # Step 1: Extract nested sections
    nested_sections = extract_sections(pdf_path)
    save_to_json(nested_sections, nested_output_path)
    print(f"Nested sections saved to {nested_output_path}")

    # Step 2: Generate paragraph chunks
    chunks = generate_chunks(nested_sections)
    save_to_json(chunks, chunks_output_path)
    print(f"Paragraph chunks saved to {chunks_output_path}")

    # Step 3: Use Chroma with Ollama embeddings
    client = chromadb.Client()
    embedding_fn = OllamaEmbeddingFunction(model_name="nomic-embed-text")  # You can change model if needed

    collection_name = "pdf_chunks"
    documents = [chunk["data"] for chunk in chunks]
    metadatas = [chunk["metadata"] for chunk in chunks]
    ids = [str(i) for i in range(len(documents))]

    collection = client.create_collection(name=collection_name, embedding_function=embedding_fn)
    collection.add(documents=documents, metadatas=metadatas, ids=ids)
    print(f"Added {len(documents)} chunks to Chroma DB")

    # Step 4: Interactive search
    while True:
        query = input("\nSearch for: ").strip()
        if query.lower() == "exit":
            break

        results = collection.query(query_texts=[query], n_results=2)
        print("\nTop 2 results:")
        for i, (doc, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
            print(f"\nResult {i + 1}")
            print(f"Text: {doc[:300]}{'...' if len(doc) > 300 else ''}")
            print(f"Metadata: {meta}")
