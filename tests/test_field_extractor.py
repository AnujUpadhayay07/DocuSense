
from pathlib import Path

from app.extractors.pdf_extractor import extract_text
from app.extractors.table_extractor import extract_tables
from app.extractors.field_extractor import extract_fields


def get_extraction_result(pdf_path):
    text_result = extract_text(pdf_path)
    table_result = extract_tables(pdf_path)

    return {
        "file_name": text_result["file_name"],
        "total_pages": text_result["total_pages"],
        "pages": text_result["pages"],
        "tables": table_result["tables"]
    }


def test_extract_structured_fields_from_scanned_pdf():
    pdf_path = Path("sample_docs/scanned_sample.pdf")

    result = get_extraction_result(pdf_path)
    fields = extract_fields(result)

    assert fields["document_type"] == "invoice"
    assert fields["invoice_number"] == "INV-2026-104"
    assert fields["currency"] == "INR"
    assert fields["total_amount"] == 25500.0


def test_extract_structured_fields_from_table_pdf():
    pdf_path = Path("sample_docs/table_sample.pdf")

    result = get_extraction_result(pdf_path)
    fields = extract_fields(result)

    assert fields["document_type"] == "invoice"
    assert fields["invoice_number"] == "INV-2026-205"
    assert fields["currency"] == "INR"
    assert fields["total_amount"] == 143500.0


def test_unknown_document_type():
    pdf_path = Path("sample_docs/sample_document.pdf")

    result = get_extraction_result(pdf_path)
    fields = extract_fields(result)

    assert fields["document_type"] == "unknown"
    assert fields["invoice_number"] is None
    assert fields["total_amount"] is None


def test_grand_total_has_priority():
    extraction_result = {
        "file_name": "priority_test.pdf",
        "total_pages": 1,
        "pages": [
            {
                "page": 1,
                "text": (
                    "Invoice Number: INV-100\n"
                    "Total Amount: INR 25000\n"
                    "Grand Total: INR 27500"
                )
            }
        ],
        "tables": []
    }

    fields = extract_fields(extraction_result)

    assert fields["total_amount"] == 27500.0
