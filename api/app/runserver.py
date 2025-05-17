def toc_to_nested_json(toc):
    root = {"title": "Document", "children": []}
    stack = [(0, root)]  # (level, node)

    for level, title, page in toc:
        node = {"title": title, "page": page, "children": []}
        # Find parent node
        while stack and stack[-1][0] >= level:
            stack.pop()
        parent_level, parent_node = stack[-1]
        parent_node["children"].append(node)
        stack.append((level, node))

    return root      import fitz  # PyMuPDF

doc = fitz.open("your_file.pdf")
toc = doc.get_toc()
nested_json = toc_to_nested_json(toc)

import json
with open("toc_nested.json", "w", encoding="utf-8") as f:
    json.dump(nested_json, f, indent=2)
