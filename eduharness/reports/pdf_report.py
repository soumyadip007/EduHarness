from __future__ import annotations

from datetime import UTC, datetime
from io import BytesIO
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def generate_summary_pdf(
    title: str,
    summary: dict,
    model_metadata: dict | None = None,
    output_path: str | Path | None = None,
) -> bytes:
    """Generate a PDF report; returns bytes and optionally writes to disk."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, title=title)
    styles = getSampleStyleSheet()
    story = [
        Paragraph(title, styles["Title"]),
        Paragraph(f"Generated: {datetime.now(UTC).isoformat()}", styles["Normal"]),
        Spacer(1, 12),
    ]

    if model_metadata:
        story.append(Paragraph("Model Configuration", styles["Heading2"]))
        model_rows = [[k.replace("_", " ").title(), str(v)] for k, v in model_metadata.items()]
        model_table = Table([["Field", "Value"], *model_rows], colWidths=[180, 320])
        model_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ]
            )
        )
        story.append(model_table)
        story.append(Spacer(1, 12))

    story.append(Paragraph("Summary Metrics", styles["Heading2"]))
    rows = [[k.replace("_", " ").title(), str(v)] for k, v in summary.items()]
    table = Table([["Metric", "Value"], *rows], colWidths=[220, 280])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ]
        )
    )
    story.append(table)
    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()

    if output_path:
        Path(output_path).write_bytes(pdf_bytes)
    return pdf_bytes
