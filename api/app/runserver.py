import fitz
import json

def extract_toc(pdf_path, max_page=7):
    doc = fitz.open(pdf_path)
    toc = doc.get_toc()  # [level, title, page]
    doc.close()
    # Filter TOC entries only within first max_page pages
    filtered_toc = [entry for entry in toc if entry[2] <= max_page]
    return filtered_toc

def toc_to_nested_json(toc):
    root = []
    stack = []

    for level, title, page in toc:
        node = {
            "title": title,
            "page": page,
            "children": []
        }

        if level == 1:
            root.append(node)
            stack = [node]
        else:
            while len(stack) >= level:
                stack.pop()
            parent = stack[-1]
            parent["children"].append(node)
            stack.append(node)

    return root

if __name__ == "__main__":
    pdf_path = "your_file.pdf"  # Change this
    toc = extract_toc(pdf_path, max_page=7)
    nested_toc = toc_to_nested_json(toc)

    with open("toc_first_7_pages.json", "w", encoding="utf-8") as f:
        json.dump(nested_toc, f, indent=2, ensure_ascii=False)

    print("Filtered TOC saved to toc_first_7_pages.json")
