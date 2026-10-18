from dataclasses import dataclass, field
from typing import Any

@dataclass
class StructuredDocument:
    file_name: str
    document_type: str = "unknown"
    total_pages: int = 0
    invoice_number: str | None = None
    currency: str | None = None
    total_amount: float | None = None
    pages: list[dict[str, Any]] = field(default_factory=list)
    tables: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "file_name": self.file_name,
            "document_type": self.document_type,
            "total_pages": self.total_pages,
            "invoice_number": self.invoice_number,
            "currency": self.currency,
            "total_amount": self.total_amount,
            "pages": self.pages,
            "tables": self.tables,
        }