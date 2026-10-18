
from pathlib import Path

import pytest

from app.extractors.table_extractor import extract_tables


def test_extract_tables_from_pdf():
    pdf_path = Path("sample_docs/table_sample.pdf")

    result = extract_tables(pdf_path)

    assert result["file_name"] == "table_sample.pdf"
    assert result["total_pages"] == 1
    assert result["total_tables"] == 1

    table = result["tables"][0]

    assert table["page"] == 1
    assert table["table_number"] == 1
    assert table["headers"] == [
        "Item",
        "Quantity",
        "Unit Price",
        "Total"
    ]

    assert table["row_count"] == 3

    assert table["data"][0] == {
        "Item": "Laptop",
        "Quantity": "2",
        "Unit Price": "50000",
        "Total": "100000"
    }


def test_extract_tables_from_pdf_with_no_tables():
    pdf_path = Path("sample_docs/sample_document.pdf")

    result = extract_tables(pdf_path)

    assert result["file_name"] == "sample_document.pdf"
    assert result["total_tables"] == 0
    assert result["tables"] == []


def test_missing_pdf_raises_error():
    pdf_path = Path("sample_docs/missing_document.pdf")

    with pytest.raises(FileNotFoundError):
        extract_tables(pdf_path)


def test_non_pdf_file_raises_error(tmp_path):
    file_path = tmp_path / "document.txt"
    file_path.write_text("Not a PDF", encoding="utf-8")

    with pytest.raises(ValueError, match="Expected a PDF file"):
        extract_tables(file_path)


def test_corrupted_pdf_raises_error(tmp_path):
    pdf_path = tmp_path / "corrupted.pdf"
    pdf_path.write_text(
        "This is not a valid PDF file",
        encoding="utf-8"
    )

    with pytest.raises(ValueError, match="Invalid or corrupted PDF"):
        extract_tables(pdf_path)
