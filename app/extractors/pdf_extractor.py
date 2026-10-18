
from pathlib import Path
from io import BytesIO

import pymupdf
import pytesseract
from PIL import Image


# Tesseract OCR executable path
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def extract_text(pdf_path):
    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    if not pdf_path.is_file():
        raise ValueError(f"Path is not a file: {pdf_path}")

    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(f"Expected a PDF file: {pdf_path}")

    try:
        with pymupdf.open(pdf_path) as pdf:
            pages_text = []

            for page_number, page in enumerate(pdf, start=1):
                # Step 1: Try extracting normal PDF text.
                text = page.get_text().strip()
                extraction_method = "text"

                # Step 2: If no selectable text exists, use OCR.
                if not text:
                    pixmap = page.get_pixmap(
                        matrix=pymupdf.Matrix(2, 2),
                        alpha=False
                    )

                    image = Image.open(
                        BytesIO(pixmap.tobytes("png"))
                    )

                    text = pytesseract.image_to_string(
                        image,
                        lang="eng"
                    ).strip()

                    extraction_method = "ocr"

                # Step 3: Store extracted text and its method.
                pages_text.append({
                    "page": page_number,
                    "text": text,
                    "extraction_method": extraction_method
                })

            return {
                "file_name": pdf_path.name,
                "total_pages": len(pdf),
                "metadata": pdf.metadata,
                "pages": pages_text
            }

    except pymupdf.FileDataError as error:
        raise ValueError(
            f"Invalid or corrupted PDF: {pdf_path}"
        ) from error
