"""Render each PDF page as a PNG image.
This guarantees 1:1 page-to-image mapping (no duplicates, no shared xrefs).
Only renders pages that contain figures/diagrams (based on image count).
"""
import sys, os, io, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import fitz

BOOKS = [
    ("1권 공공조달의 이해.pdf", "book1"),
    ("2권 공공조달 계획분석.pdf", "book2"),
    ("3권 공공계약관리.pdf", "book3"),
    ("4권 공공조달 관리실무.pdf", "book4"),
]

BASE = os.path.join(os.path.dirname(__file__), "..", "sources", "textbooks")
IMG_OUT = os.path.join(os.path.dirname(__file__), "..", "web", "public", "images", "textbook")

# Clear old images
if os.path.exists(IMG_OUT):
    shutil.rmtree(IMG_OUT)
os.makedirs(IMG_OUT, exist_ok=True)

for pdf_name, book_id in BOOKS:
    pdf_path = os.path.join(BASE, pdf_name)
    if not os.path.exists(pdf_path):
        print(f"SKIP: {pdf_name}")
        continue

    doc = fitz.open(pdf_path)
    print(f"\n=== {pdf_name}: {len(doc)} pages ===")

    img_dir = os.path.join(IMG_OUT, book_id)
    os.makedirs(img_dir, exist_ok=True)

    # Render each page as a PNG (150 DPI for good quality without excessive size)
    zoom = 150 / 72  # 150 DPI
    matrix = fitz.Matrix(zoom, zoom)

    rendered = 0
    for i in range(len(doc)):
        page = doc[i]
        # Only render if page has at least one image (indicating diagrams/figures)
        # OR if it's likely a visual-heavy page (small text)
        img_list = page.get_images(full=True)
        has_image = len(img_list) > 0

        if not has_image:
            continue

        # Render the full page
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        out_path = os.path.join(img_dir, f"p{i+1}.png")
        pix.save(out_path)
        rendered += 1
        pix = None

    print(f"  Rendered: {rendered} pages (with figures) to {img_dir}")
    doc.close()

print("\nDone!")
