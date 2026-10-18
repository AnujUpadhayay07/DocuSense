from pathlib import Path
import pymupdf

output_path = Path("sample_docs/scanned_sample.pdf")
output_path.parent.mkdir(parents=True, exist_ok=True)

# Create a temporary page containing sample text.
with pymupdf.open() as source_pdf:
    page = source_pdf.new_page(width=595, height=842)

    page.insert_text(
        (60, 100),
        "DocuSense Scanned Document",
        fontsize=20
    )
    page.insert_text(
        (60, 150),
        "This text is stored as an image, not selectable text.",
        fontsize=12
    )
    page.insert_text(
        (60, 190),
        "Invoice Number: INV-2026-104",
        fontsize=14
    )
    page.insert_text(
        (60, 225),
        "Total Amount: INR 25,500",
        fontsize=14
    )

    # Render the page as an image.
    pixmap = page.get_pixmap(
        matrix=pymupdf.Matrix(2, 2),
        alpha=False
    )
    image_bytes = pixmap.tobytes("png")

# Create a new PDF containing only that image.
with pymupdf.open() as scanned_pdf:
    scanned_page = scanned_pdf.new_page(
        width=pixmap.width,
        height=pixmap.height
    )
    scanned_page.insert_image(
        scanned_page.rect,
        stream=image_bytes
    )
    scanned_pdf.save(output_path)

print(f"Scanned sample created: {output_path.resolve()}")
