import fitz  # PyMuPDF
import json

def get_sorted_toc(pdf_path, max_page=7):
    doc = fitz.open(pdf_path)
    toc = doc.get_toc()

    # Filter entries within first `max_page` pages
    filtered_toc = [entry for entry in toc if entry[2] <= max_page]

    # Sort by page number
    sorted_toc = sorted(filtered_toc, key=lambda x: x[2])

    # Build nested hierarchy
    hierarchy = []
    stack = []

    for level, title, page in sorted_toc:
        node = {
            "title": title.strip(),
            "page": page,
            "children": []
        }

        if level == 1:
            hierarchy.append(node)
            stack = [node]
        else:
            while len(stack) >= level:
                stack.pop()
            if stack:
                stack[-1]["children"].append(node)
            stack.append(node)

    return hierarchy

# Usage
pdf_path = "your_file.pdf"
toc_hierarchy = get_sorted_toc(pdf_path)

# Write to JSON file
with open("toc_output.json", "w", encoding="utf-8") as f:
    json.dump(toc_hierarchy, f, indent=2, ensure_ascii=False)

print("ToC JSON saved to toc_output.json")
