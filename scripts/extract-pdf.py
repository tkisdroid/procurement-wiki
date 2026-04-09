"""Extract text and images from all 4 textbook PDFs."""
import sys, os, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import fitz  # pymupdf

BOOKS = [
    ("1권 공공조달의 이해.pdf", "book1"),
    ("2권 공공조달 계획분석.pdf", "book2"),
    ("3권 공공계약관리.pdf", "book3"),
    ("4권 공공조달 관리실무.pdf", "book4"),
]

BASE = os.path.join(os.path.dirname(__file__), "..", "sources", "textbooks")
OUT = os.path.join(os.path.dirname(__file__), "..", "sources", "extracted")
IMG_OUT = os.path.join(os.path.dirname(__file__), "..", "web", "public", "images", "textbook")

os.makedirs(OUT, exist_ok=True)
os.makedirs(IMG_OUT, exist_ok=True)

for pdf_name, book_id in BOOKS:
    pdf_path = os.path.join(BASE, pdf_name)
    if not os.path.exists(pdf_path):
        print(f"SKIP: {pdf_name} not found")
        continue

    doc = fitz.open(pdf_path)
    print(f"\n=== {pdf_name}: {len(doc)} pages ===")

    # Extract text
    text_parts = []
    for i, page in enumerate(doc):
        text = page.get_text()
        if text.strip():
            text_parts.append(f"\n<!-- Page {i+1} -->\n{text}")

    out_file = os.path.join(OUT, f"{book_id}.md")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(text_parts))
    print(f"  Text: {out_file} ({len(text_parts)} pages with text)")

    # Extract images
    img_dir = os.path.join(IMG_OUT, book_id)
    os.makedirs(img_dir, exist_ok=True)
    img_count = 0
    for i, page in enumerate(doc):
        for j, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            try:
                pix = fitz.Pixmap(doc, xref)
                if pix.n > 4:  # CMYK
                    pix = fitz.Pixmap(fitz.csRGB, pix)
                ext = "png" if pix.alpha else "png"
                img_path = os.path.join(img_dir, f"p{i+1}_img{j+1}.png")
                pix.save(img_path)
                img_count += 1
                pix = None
            except Exception as e:
                pass
    print(f"  Images: {img_count} extracted to {img_dir}")

    doc.close()

print("\nDone!")
