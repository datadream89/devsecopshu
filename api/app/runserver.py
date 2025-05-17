import pdfplumber
import re
import json
from collections import defaultdict
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction
from langchain.vectorstores import Chroma

QUOTE_PAIRS = [
    ('"', '"'), ('“', '”'), ('„', '“'), ('«', '»'), ('‹', '›'), ('‟', '”'),
    ('❝', '❞'), ('〝', '〞'), ('＂', '＂')
]

def extract_title_and_rest(text):
    text = text.strip()
    for open_q, close_q in QUOTE_PAIRS:
        pattern = re.escape(open_q) + r'(.+?)' + re.escape(close_q)
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip(), text.replace(match.group(0), '').strip()
    return None, text

section_header_re = re.compile(
    r"""^\s*
    (?P<header>
        (?:\d+(?:\.\d+)*\.)     # e.g. 1. or 1.1. or 2.6.4.
        | [a-zA-Z]\.               # e.g. a. or B.
        | \([a-zA-Z0-9]+\)        # e.g. (a), (1)
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
    return h.split('.')

def insert_section(root, section_numbers, section_data):
    current = root
    for i, part in enumerate(section_numbers):
        if "children" not in current:
            current["children"] = {}

        key = part
        if key not in current["children"]:
            current["children"][key] = {
                "section_header": part + ('.' if not part.endswith('.') else ''),
                "paragraph": "",
                "page": [],
            }
        current = current["children"][key]

        if i == len(section_numbers) - 1:
            for k, v in section_data.items():
                if k == "paragraph":
                    current[k] += (v + "\n")
                elif k == "page":
                    current[k] = sorted(set(current.get("page", []) + v))
                else:
                    current[k] = v

def flatten_tree(node):
    def helper(node):
        res = {}
        for k in ("page", "section_header", "topic", "section_title", "paragraph"):
            if k in node:
                res[k] = node[k].strip() if isinstance(node[k], str) else node[k]
        if "children" in node:
            res["children"] = [helper(child) for key, child in sorted(node["children"].items())]
        return res
    return helper(node)

def extract_sections(pdf_path):
    root = {"section_header": "root", "paragraph": "", "children": {}}
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
                        "page": [page_num],
                        "section_header": header
                    }

                    title, rest = extract_title_and_rest(rest_of_line)
                    if title:
                        if is_top_level_section(header):
                            current_section_data["topic"] = title
                        else:
                            current_section_data["section_title"] = title
                    paragraph_start = rest.strip()
                    if paragraph_start:
                        buffer.append(paragraph_start)
                else:
                    if current_section_numbers:
                        buffer.append(line)
                        if page_num not in current_section_data["page"]:
                            current_section_data["page"].append(page_num)

        flush()

    return flatten_tree(root)

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

# ---------- Main Program ----------

if __name__ == "__main__":
    pdf_path = "your_file.pdf"  # Change this
    nested_output_path = "nested_output.json"
    chunks_output_path = "chunks.json"

    nested_data = extract_sections(pdf_path)
    save_to_json(nested_data, nested_output_path)

    chunks = generate_chunks(nested_data)
    save_to_json(chunks, chunks_output_path)

    embedding_fn = OllamaEmbeddingFunction(model_name="nomic-embed-text")
    documents = [chunk["data"] for chunk in chunks]
    metadatas = [chunk["metadata"] for chunk in chunks]

    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embedding_fn,
        metadatas=metadatas,
        collection_name="pdf_chunks"
    )

    print(f"{len(documents)} chunks embedded and stored in Chroma.")

    while True:
        query = input("\nSearch for (type 'exit' to quit): ").strip()
        if query.lower() == "exit":
            break

        results = vector_store.similarity_search(query, k=2)
        selected = None
        defs = [r for r in results if 'topic' in r.metadata and 'definition' in r.metadata['topic'].lower()]

        if len(defs) == 2:
            selected = defs[0]
        elif len(defs) == 1:
            selected = defs[0]
        else:
            selected = results[0]

        print("\nTop Result:")
        print(f"Text: {selected.page_content[:300]}{'...' if len(selected.page_content) > 300 else ''}")
        print(f"Metadata: {selected.metadata}")
