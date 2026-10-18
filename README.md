# DocuSense — Multimodal Document Intelligence

DocuSense is a Python-based document intelligence project that extracts text, tables, and structured information from PDF documents, including scanned PDFs.

The project provides a FastAPI interface for uploading PDFs and receiving extracted information in JSON format.

## Features

- **PDF Text Extraction:** Extract selectable text from digital PDFs.
- **OCR:** Extract text from scanned PDF pages using Tesseract OCR.
- **Table Extraction:** Detect tables and return headers and rows as structured data.
- **Structured Field Extraction:** Identify document types and extract invoice numbers, currencies, and total amounts using rule-based patterns.
- **REST API:** Upload PDF files and retrieve results through FastAPI.
- **Automated Tests:** Validate extraction logic and error handling using pytest.

## Tech Stack

- Python
- FastAPI
- Uvicorn
- PyMuPDF
- pypdf
- Tesseract OCR
- pytesseract
- Pillow
- pytest

## Project Structure

```text
DocuSense/
├── app/
│   ├── api/
│   ├── extractors/
│   └── schemas/
├── sample_docs/
├── tests/
├── output/
├── requirements.txt
└── README.md
```

## Prerequisites

- Python 3.13 or a compatible Python version
- Tesseract OCR installed for scanned PDF extraction

Install Tesseract OCR for Windows from the official project:
https://github.com/tesseract-ocr/tesseract

Make sure the Tesseract executable is accessible to the application.

## Installation

Clone the repository and enter the project directory:

```powershell
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd DocuSense
```

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Run the API

From the project root, run:

```powershell
python -m uvicorn app.api.main:app --reload
```

Open the interactive API documentation:

http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API welcome message |
| GET | `/health` | Health check |
| POST | `/extract` | Extract information from an uploaded PDF |

### Extract a PDF

1. Open `/docs` in your browser.
2. Expand `POST /extract`.
3. Click **Try it out**.
4. Select a PDF file and click **Execute**.

The API returns extracted text, page information, detected tables, and structured fields as JSON.

Example structured output:

```json
{
  "document_type": "project_proposal",
  "invoice_number": "INV-TEST-2026-01",
  "currency": "INR",
  "total_amount": 65000.0
}
```

The example demonstrates the expected output for a test document; actual fields depend on the PDF content and the extraction rules.

## Run Tests

Run the complete test suite:

```powershell
python -m pytest -v
```

The current test suite contains 14 passing tests covering PDF extraction, OCR, table extraction, structured fields, and error handling.

## Current Limitations

- Document classification currently uses rule-based text patterns.
- Structured field extraction supports a limited set of fields and currencies.
- Table detection and OCR accuracy depend on the PDF layout and scan quality.
- Tesseract OCR must be installed separately from Python dependencies.

## Future Improvements

- Improve document classification and structured field extraction.
- Add support for more document types and field schemas.
- Improve handling of complex tables and mixed text/image pages.
- Add a frontend for document upload and result visualization.
- Add document-grounded question answering with page references.

## License

A license has not yet been specified.
