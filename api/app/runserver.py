import pdfplumber
import re
import json

def is_probable_title(text):
    # Heuristic: title if short + quoted/uppercase-ish/keyword-like
    return (
        len(text.split()) <= 8 and (
            text.startswith('"') and text.endswith('"') or
            text.startswith("'") and text.endswith("'") or
            text.isupper() or
            text.istitle()
        )
    )

def extract_sections(pdf_path):
    # Match section headers
    section_pattern = re.compile(
        r"""^\s*
        (?P<header>
            (?:\d+(?:\.\d+)*\.)     # 1., 1.1., 2.3.4.
            | [a-zA-Z]\.            # a., B., z.
            | \([a-zA-Z0-9]+\)      # (a), (1), (B)
        )
        \s*
        (?P<title>.*)?             # Optional trailing title
        $""", re.VERBOSE
    )

    sections = []
    current = None
    buffer = []

    def flush():
        if current and buffer:
            current["paragraph"] = "\n".join(buffer).strip()
            sections.append(current.copy())
            buffer.clear()

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            lines = text.split("\n")
            for line in lines:
                line = line.strip()
                match = section_pattern.match(line)
                if match:
                    flush()
                    header = match.group("header").strip()
                    maybe_title = (match.group("title") or "").strip()
                    current = {
                        "page": page_num,
                        "section_header": header
                    }
                    if maybe_title and is_probable_title(maybe_title):
                        current["title"] = maybe_title
                elif current:
                    buffer.append(line)

        flush()

    return sections

def save_to_json(data, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ======= Example usage =======
if __name__ == "__main__":
    pdf_path = "your_file.pdf"  # Replace with your input file
    output_path = "sections_with_titles.json"

    results = extract_sections(pdf_path)
    save_to_json(results, output_path)

    print(f"Done. Results saved to {output_path}")
