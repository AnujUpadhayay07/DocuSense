
import json
from pathlib import Path

import pytest

from app.extractors.pdf_extractor import extract_text


def test_extract_text_from_pdf():
    pdf_path = Path("sample_docs/sample_document.pdf")

    result = extract_text(pdf_path)

    assert result["file_name"] == "sample_document.pdf"
    assert result["total_pages"] == 1
    assert len(result["pages"]) == 1
    assert result["pages"][0]["page"] == 1
    assert "DocuSense Sample Document" in result["pages"][0]["text"]
    assert "Document Intelligence - Milestone 1" in result["pages"][0]["text"]
    assert result["pages"][0]["extraction_method"] == "text"
    assert isinstance(result["metadata"], dict)


def test_extract_text_from_scanned_pdf():
    pdf_path = Path("sample_docs/scanned_sample.pdf")

    result = extract_text(pdf_path)

    assert result["file_name"] == "scanned_sample.pdf"
    assert result["total_pages"] == 1

    extracted_text = result["pages"][0]["text"]

    assert "DocuSense Scanned Document" in extracted_text
    assert "INV-2026-104" in extracted_text
    assert "25,500" in extracted_text
    assert result["pages"][0]["extraction_method"] == "ocr"


def test_missing_pdf_raises_error():
    pdf_path = Path("sample_docs/missing_document.pdf")

    with pytest.raises(FileNotFoundError):
        extract_text(pdf_path)


def test_corrupted_pdf_raises_error(tmp_path):
    pdf_path = tmp_path / "corrupted.pdf"
    pdf_path.write_text(
        "This is not a valid PDF file",
        encoding="utf-8"
    )

    with pytest.raises(ValueError, match="Invalid or corrupted PDF"):
        extract_text(pdf_path)


def test_json_output_contains_extracted_data(tmp_path):
    pdf_path = Path("sample_docs/sample_document.pdf")
    result = extract_text(pdf_path)

    json_path = tmp_path / "sample_document.json"
    json_path.write_text(
        json.dumps(result, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )

    saved_result = json.loads(
        json_path.read_text(encoding="utf-8")
    )

    assert saved_result["file_name"] == "sample_document.pdf"
    assert saved_result["total_pages"] == 1
    assert saved_result["pages"][0]["page"] == 1
    assert "DocuSense Sample Document" in saved_result["pages"][0]["text"]
