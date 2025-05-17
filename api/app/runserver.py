def toc_to_nested_json(toc):
    root = {"title": "Document", "children": []}
    stack = [(0, root)]  # (level, node)

    for entry in toc:
        if len(entry) < 3:
            continue  # skip invalid entries

        level, title, page = entry[:3]  # safely unpack only the first 3

        node = {"title": title, "page": page, "children": []}

        while stack and stack[-1][0] >= level:
            stack.pop()

        parent_level, parent_node = stack[-1]
        parent_node["children"].append(node)
        stack.append((level, node))

    return root
