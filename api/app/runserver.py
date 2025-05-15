import fitz

def find_closest_paragraph_string_to_term(pdf_path, para1, para2, target_term):
    doc = fitz.open(pdf_path)

    paras = [para1.strip(), para2.strip()]
    para_matches = []

    # Step 1: Find positions of both paragraphs in the PDF
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("blocks")
        for block in blocks:
            text = block[4].strip()
            for para in paras:
                if para in text:
                    para_matches.append({
                        "text": para,
                        "page": page_num,
                        "bbox": block[:4]
                    })

    # Step 2: Find all blocks containing the target term
    target_locs = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("blocks")
        for block in blocks:
            if target_term.lower() in block[4].lower():
                target_locs.append({
                    "page": page_num,
                    "bbox": block[:4]
                })

    # Step 3: Find closest paragraph to target term
    def get_distance(b1, b2):
        cx1, cy1 = (b1[0] + b1[2]) / 2, (b1[1] + b1[3]) / 2
        cx2, cy2 = (b2[0] + b2[2]) / 2, (b2[1] + b2[3]) / 2
        return ((cx1 - cx2) ** 2 + (cy1 - cy2) ** 2) ** 0.5

    closest_para = None
    min_distance = float("inf")

    for para in para_matches:
        for target in target_locs:
            if para["page"] == target["page"]:
                dist = get_distance(para["bbox"], target["bbox"])
                if dist < min_distance:
                    min_distance = dist
                    closest_para = {**para, "distance": round(dist, 2)}

    return closest_para
