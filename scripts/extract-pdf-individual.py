"""Extract individual images from PDFs using PyMuPDF.
Based on eduland_heavy_parser.py approach:
- Filter out small icons (< 50x50)
- Save each image individually with meaningful name
- Keep structured markdown for text
"""
import sys, os, io, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import fitz
from PIL import Image
from io import BytesIO

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

MIN_SIZE = 50  # Filter out icons smaller than 50x50

for pdf_name, book_id in BOOKS:
    pdf_path = os.path.join(BASE, pdf_name)
    if not os.path.exists(pdf_path):
        print(f"SKIP: {pdf_name}")
        continue

    doc = fitz.open(pdf_path)
    print(f"\n=== {pdf_name}: {len(doc)} pages ===")

    img_dir = os.path.join(IMG_OUT, book_id)
    os.makedirs(img_dir, exist_ok=True)

    total_saved = 0
    total_filtered = 0

    for page_num in range(len(doc)):
        page = doc[page_num]
        img_list = page.get_images(full=True)

        saved_on_page = 0
        for img_idx, img_info in enumerate(img_list, 1):
            xref = img_info[0]
            try:
                base_image = doc.extract_image(xref)
                if not base_image or not base_image.get("image"):
                    continue

                img_bytes = base_image["image"]
                img_ext = base_image.get("ext", "png")

                # Load with PIL to check size
                pil_img = Image.open(BytesIO(img_bytes))
                w, h = pil_img.size

                # Filter out small icons
                if w < MIN_SIZE or h < MIN_SIZE:
                    total_filtered += 1
                    continue

                # Save with meaningful name: p{page}_fig{index}.{ext}
                img_name = f"p{page_num+1}_fig{saved_on_page+1}.{img_ext}"
                out_path = os.path.join(img_dir, img_name)

                # Normalize extension to png if possible
                if img_ext.lower() in ("jb2", "jpx", "jpeg2000"):
                    # Convert to PNG
                    pil_img.save(out_path.replace(f".{img_ext}", ".png"))
                else:
                    with open(out_path, "wb") as f:
                        f.write(img_bytes)

                saved_on_page += 1
                total_saved += 1
            except Exception as e:
                pass

    print(f"  Saved: {total_saved} images, filtered: {total_filtered} small icons")
    doc.close()

print("\nDone!")
