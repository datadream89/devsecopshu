import fitz  # PyMuPDF
import os

def split_pdf_by_blocks(pdf_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    doc = fitz.open(pdf_path)

    para_count = 0
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("blocks")  # returns list of (x0, y0, x1, y1, "text", block_no, block_type)

        for block in blocks:
            text = block[4].strip()
            if not text:
                continue
            # Optional: filter out headers/footers or non-text blocks
            para_doc = fitz.open()
            para_page = para_doc.new_page()
            para_page.insert_text((72, 72), text, fontsize=11)
            para_doc.save(os.path.join(output_dir, f"paragraph_{para_count:03}.pdf"))
            para_doc.close()
            para_count += 1

    print(f"Saved {para_count} blocks in '{output_dir}'")

# Example usage
split_pdf_by_blocks("example.pdf", "output_blocks")
