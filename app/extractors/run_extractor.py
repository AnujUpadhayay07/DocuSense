
import argparse
import json
from pathlib import Path

from app.extractors.pdf_extractor import extract_text
from app.extractors.table_extractor import extract_tables
from app.extractors.field_extractor import extract_fields


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Extract PDF text, OCR, tables and structured fields."
        )
    )

    parser.add_argument(
        "pdf_path",
        help="Path to the PDF file to process"
    )

    args = parser.parse_args()
    pdf_path = Path(args.pdf_path)

    try:
        # Step 1: Extract text, metadata and OCR results.
        text_result = extract_text(pdf_path)

        # Step 2: Extract tables.
        table_result = extract_tables(pdf_path)

        # Step 3: Combine the extraction results.
        result = {
            "file_name": text_result["file_name"],
            "total_pages": text_result["total_pages"],
            "metadata": text_result["metadata"],
            "pages": text_result["pages"],
            "total_tables": table_result["total_tables"],
            "tables": table_result["tables"]
        }

        # Step 4: Extract structured document fields.
        structured_result = extract_fields(result)
        result["structured_data"] = {
            "document_type": structured_result["document_type"],
            "invoice_number": structured_result["invoice_number"],
            "currency": structured_result["currency"],
            "total_amount": structured_result["total_amount"]
        }

        # Step 5: Save the complete result as JSON.
        output_dir = Path("output")
        output_dir.mkdir(parents=True, exist_ok=True)

        json_path = output_dir / f"{pdf_path.stem}.json"

        with json_path.open("w", encoding="utf-8") as json_file:
            json.dump(
                result,
                json_file,
                indent=4,
                ensure_ascii=False
            )

        # Step 6: Display the extraction summary.
        print("\n========== DocuSense Document Extraction ==========")
        print(f"File name: {result['file_name']}")
        print(f"Total pages: {result['total_pages']}")

        metadata = result["metadata"]
        print(f"Title: {metadata.get('title') or 'Not available'}")
        print(f"Author: {metadata.get('author') or 'Not available'}")

        for page in result["pages"]:
            print(f"\n--- Page {page['page']} ---")
            print(f"Method: {page['extraction_method']}")
            print(page["text"] or "[No text detected on this page]")

        print(f"\nTotal tables detected: {result['total_tables']}")

        for table in result["tables"]:
            print(
                f"Page {table['page']}, "
                f"Table {table['table_number']}: "
                f"{table['row_count']} data rows"
            )

        print("\n--- Structured Data ---")
        for key, value in result["structured_data"].items():
            print(f"{key}: {value}")

        print(f"\nJSON output saved to: {json_path}")
        print("Extraction completed successfully.")

    except (FileNotFoundError, ValueError) as error:
        print(f"\nExtraction failed: {error}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
