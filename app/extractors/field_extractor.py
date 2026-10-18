
import re

from app.schemas.document_schema import StructuredDocument


def extract_fields(extraction_result):
    # Step 1: Combine text from all pages.
    pages = extraction_result.get("pages", [])

    full_text = "\n".join(
        page.get("text", "")
        for page in pages
    )

    # Step 2: Extract invoice number.
    invoice_match = re.search(
        r"\bInvoice\s*(?:Number|No\.?|#)\s*[:\-]?\s*([A-Z0-9\-]+)",
        full_text,
        re.IGNORECASE
    )

    invoice_number = (
        invoice_match.group(1)
        if invoice_match
        else None
    )

    # Step 3: Extract currency.
    currency_match = re.search(
        r"\b(INR|USD|EUR|GBP)\b",
        full_text,
        re.IGNORECASE
    )

    currency = (
        currency_match.group(1).upper()
        if currency_match
        else None
    )

    # Step 4: Extract the labelled total amount.
    # Prefer Grand Total over Total Amount.
    total_amount = None

    amount_patterns = [
        r"\bGrand\s+Total\s*[:\-]?\s*"
        r"(?:INR|USD|EUR|GBP)?\s*"
        r"([0-9,]+(?:\.[0-9]{1,2})?)",

        r"\bTotal\s+Amount\s*[:\-]?\s*"
        r"(?:INR|USD|EUR|GBP)?\s*"
        r"([0-9,]+(?:\.[0-9]{1,2})?)"
    ]

    for pattern in amount_patterns:
        amount_match = re.search(
            pattern,
            full_text,
            re.IGNORECASE
        )

        if amount_match:
            amount_text = amount_match.group(1).replace(",", "")
            total_amount = float(amount_text)
            break

    # Step 5: Fallback to the table's Total column
    # only when no labelled amount was found.
    if total_amount is None:
        for table in extraction_result.get("tables", []):
            headers = table.get("headers", [])

            total_header = next(
                (
                    header
                    for header in headers
                    if isinstance(header, str)
                    and header.strip().lower() == "total"
                ),
                None
            )

            if total_header is None:
                continue

            values = []

            for row in table.get("data", []):
                value = row.get(total_header)

                if value is None:
                    continue

                try:
                    numeric_value = float(
                        str(value).replace(",", "").strip()
                    )
                    values.append(numeric_value)
                except (ValueError, TypeError):
                    continue

            if values:
                total_amount = sum(values)
                break

    # Step 6: Identify document type.
    # An explicitly stated document type takes priority
    # over invoice-related words elsewhere in the document.
    document_type = "unknown"

    explicit_type_patterns = [
        (
            r"\b(?:document\s+type|type\s+of\s+document)"
            r"\s*[:\-]\s*project\s+proposal\b",
            "project_proposal"
        ),
        (
            r"\bproject\s+proposal\b",
            "project_proposal"
        ),
        (
            r"\b(?:document\s+type|type\s+of\s+document)"
            r"\s*[:\-]\s*invoice\b",
            "invoice"
        ),
    ]

    for pattern, detected_type in explicit_type_patterns:
        if re.search(pattern, full_text, re.IGNORECASE):
            document_type = detected_type
            break

    # If no proposal or explicit type was found,
    # use invoice indicators as a fallback.
    if document_type == "unknown":
        if invoice_number or re.search(
            r"\binvoice\b",
            full_text,
            re.IGNORECASE
        ):
            document_type = "invoice"

    # Step 7: Build the structured document.
    document = StructuredDocument(
        file_name=extraction_result["file_name"],
        document_type=document_type,
        total_pages=extraction_result["total_pages"],
        invoice_number=invoice_number,
        currency=currency,
        total_amount=total_amount,
        pages=pages,
        tables=extraction_result.get("tables", [])
    )

    # Step 8: Return the structured data as a dictionary.
    return document.to_dict()
