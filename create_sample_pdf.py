from pathlib import Path
import fitz

output_path = Path("sample_docs/sample_document.pdf")

with fitz.open() as pdf:
    page = pdf.new_page()
    page.insert_text((72, 72), "DocuSense Sample Document")
    page.insert_text((72, 110), "This is a test PDF for text extraction.")
    page.insert_text((72, 145), "Document Intelligence - Milestone 1")

    pdf.save(output_path)

print(f"Sample PDF created: {output_path.resolve()}")
