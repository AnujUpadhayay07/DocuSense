
import json
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile

from app.extractors.pdf_extractor import extract_text
from app.extractors.table_extractor import extract_tables
from app.extractors.field_extractor import extract_fields


app = FastAPI(
    title="DocuSense API",
    description=(
        "Multimodal Document Intelligence API "
        "for PDF text, OCR, tables and structured fields."
    ),
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to DocuSense API",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/extract")
async def extract_document(file: UploadFile = File(...)):
    # Step 1: Validate the uploaded file name.
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF file."
        )

    if Path(file.filename).suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    # Step 2: Read the uploaded file.
    content = await file.read()

    if not content:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty."
        )

    # Step 3: Save temporarily and run existing extractors.
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            pdf_path = Path(temp_dir) / "uploaded_document.pdf"
            pdf_path.write_bytes(content)

            text_result = extract_text(pdf_path)
            table_result = extract_tables(pdf_path)

            result = {
                "file_name": Path(file.filename).name,
                "total_pages": text_result["total_pages"],
                "metadata": text_result["metadata"],
                "pages": text_result["pages"],
                "total_tables": table_result["total_tables"],
                "tables": table_result["tables"]
            }

            structured_result = extract_fields(result)

            result["structured_data"] = {
                "document_type": structured_result["document_type"],
                "invoice_number": structured_result["invoice_number"],
                "currency": structured_result["currency"],
                "total_amount": structured_result["total_amount"]
            }

            return result

    except (FileNotFoundError, ValueError) as error:
        raise HTTPException(
            status_code=422,
            detail=str(error)
        ) from error

    finally:
        await file.close()
