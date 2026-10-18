
from pathlib import Path

import pymupdf


def extract_tables(pdf_path):
    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    if not pdf_path.is_file():
        raise ValueError(f"Path is not a file: {pdf_path}")

    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(f"Expected a PDF file: {pdf_path}")

    try:
        with pymupdf.open(pdf_path) as pdf:
            extracted_tables = []

            for page_number, page in enumerate(pdf, start=1):
                # Detect tables on the current page.
                table_finder = page.find_tables()

                for table_number, table in enumerate(
                    table_finder.tables,
                    start=1
                ):
                    rows = table.extract()

                    if not rows:
                        continue

                    # Use the first row as column headers.
                    headers = [
                        str(header).strip() if header is not None else ""
                        for header in rows[0]
                    ]

                    # Convert remaining rows into dictionaries.
                    data = []

                    for row in rows[1:]:
                        row_data = {}

                        for column_index, header in enumerate(headers):
                            value = (
                                row[column_index]
                                if column_index < len(row)
                                else None
                            )

                            row_data[header or f"column_{column_index + 1}"] = (
                                str(value).strip()
                                if value is not None
                                else None
                            )

                        data.append(row_data)

                    extracted_tables.append({
                        "page": page_number,
                        "table_number": table_number,
                        "headers": headers,
                        "row_count": len(data),
                        "data": data
                    })

            return {
                "file_name": pdf_path.name,
                "total_pages": len(pdf),
                "total_tables": len(extracted_tables),
                "tables": extracted_tables
            }

    except pymupdf.FileDataError as error:
        raise ValueError(
            f"Invalid or corrupted PDF: {pdf_path}"
        ) from error
