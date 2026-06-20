from __future__ import annotations

from typing import Dict

from weasyprint import HTML


def generate_combined_pdf(html_docs: Dict[str, str]) -> bytes:
    """Combine rendered HTML report sections into one PDF document."""
    sections = []
    for title, html in html_docs.items():
        sections.append(
            f"""
            <section class="report-section">
                {html}
            </section>
            """
        )

    combined_html = f"""
    <!doctype html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            @page {{
                size: A4;
                margin: 0;
            }}
            .report-section {{
                break-after: page;
            }}
            .report-section:last-child {{
                break-after: auto;
            }}
        </style>
    </head>
    <body>
        {''.join(sections)}
    </body>
    </html>
    """

    return HTML(string=combined_html).write_pdf()
