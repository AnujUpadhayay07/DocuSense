
from pathlib import Path

import pymupdf


output_path = Path("sample_docs/table_sample.pdf")
output_path.parent.mkdir(parents=True, exist_ok=True)

with pymupdf.open() as pdf:
    page = pdf.new_page(width=595, height=842)

    page.insert_text(
        (50, 50),
        "DocuSense - Invoice Sample",
        fontsize=20
    )

    page.insert_text(
        (50, 90),
        "Invoice Number: INV-2026-205",
        fontsize=12
    )

    page.insert_text(
        (50, 115),
        "Currency: INR",
        fontsize=12
    )

    # Table layout
    x_positions = [50, 230, 330, 430, 545]
    y_positions = [170, 210, 250, 290, 330]

    headers = ["Item", "Quantity", "Unit Price", "Total"]

    rows = [
        ["Laptop", "2", "50000", "100000"],
        ["Monitor", "3", "12000", "36000"],
        ["Keyboard", "5", "1500", "7500"]
    ]

    # Draw horizontal lines.
    for y in y_positions:
        page.draw_line(
            (x_positions[0], y),
            (x_positions[-1], y),
            color=(0, 0, 0),
            width=1
        )

    # Draw vertical lines.
    for x in x_positions:
        page.draw_line(
            (x, y_positions[0]),
            (x, y_positions[-1]),
            color=(0, 0, 0),
            width=1
        )

    # Write table headers.
    for index, header in enumerate(headers):
        page.insert_text(
            (x_positions[index] + 5, 195),
            header,
            fontsize=9
        )

    # Write table rows.
    for row_index, row in enumerate(rows):
        y = 235 + row_index * 40

        for column_index, value in enumerate(row):
            page.insert_text(
                (x_positions[column_index] + 5, y),
                value,
                fontsize=10
            )

    pdf.save(output_path)

print(f"Table sample created: {output_path.resolve()}")
