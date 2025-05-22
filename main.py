from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
import os
from datetime import datetime
import uuid
from io import BytesIO

def generate_report(analysis_result: dict) -> dict:
    reports_dir = "reports"
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    filename = f"compliance_report_{timestamp}_{unique_id}.pdf"
    filepath = os.path.join(reports_dir, filename)

    if not analysis_result:
        return {"status": "failed", "error": "Missing analysis data"}

    result = analysis_result
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Custom styles
    h1 = styles["Heading1"]
    h2 = styles["Heading2"]
    h3 = styles["Heading3"]
    normal = styles["BodyText"]
    spacer = Spacer(1, 12)

    # Title
    story.append(Paragraph("Compliance Report", h1))
    story.append(spacer)

    # Scores and rating
    story.append(Paragraph(
        f"<b>Client:</b> {result.get('client_name', 'N/A')}<br/>"
        f"<b>Overall Compliance Score:</b> {result.get('overall_compliance_score', 'N/A')}<br/>"
        f"<b>Engine Compliance Score:</b> {result.get('engine_compliance_score', 'N/A')}<br/>"
        f"<b>Compliance Rating:</b> {result.get('compliance_rating', 'N/A')}",
        normal
    ))
    story.append(spacer)

    # Summary
    story.append(Paragraph("1. Summary", h2))
    story.append(Paragraph(result.get("summary", "N/A"), normal))
    story.append(spacer)

    # Section 1: Dates
    story.append(Paragraph("2. Engagement Dates", h2))
    story.append(_dict_to_table(result.get("section_1_dates", {}), styles))
    story.append(spacer)

    # Sections 2–5
    section_map = {
        2: "disclosure",
        3: "research",
        4: "suitability",
        5: "risks"
    }

    for sec in range(2, 6):
        section_key = f"section_{sec}_{section_map[sec]}"
        section_title = section_map[sec].replace("_", " ").title()
        story.append(Paragraph(f"Section {sec}: {section_title}", h2))
        story.append(_dict_to_table(result.get(section_key, {}), styles))
        story.append(spacer)

    # Compliance Issues
    story.append(Paragraph("3. Compliance Issues", h2))
    issues_data = [["Severity", "Description", "Regulation", "Recommendation"]]

    for issue in result.get("issues", []):
        sev_color_html = {
            "high": "red",
            "medium": "orange",
            "low": "green"
        }.get(issue.get("severity", "").lower(), "black")

        severity = f"<font color='{sev_color_html}'><b>{issue.get('severity', 'N/A').title()}</b></font>"
        issues_data.append([
            Paragraph(severity, normal),
            Paragraph(issue.get("description", "N/A"), normal),
            Paragraph(issue.get("regulation", "N/A"), normal),
            Paragraph(issue.get("recommendation", "N/A"), normal)
        ])

    issues_table = Table(issues_data, colWidths=[80, 150, 120, 120], repeatRows=1)
    issues_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(issues_table)
    story.append(spacer)

    # Evidence Summary
    story.append(Paragraph("4. Evidence Summary", h2))
    for section, fields in result.get("evidence", {}).items():
        story.append(Paragraph(section.replace("_", " ").title(), h3))
        story.append(_dict_to_table(fields, styles))
        story.append(spacer)

    doc.build(story)
    pdf_buffer.seek(0)

    with open(filepath, "wb") as f:
        f.write(pdf_buffer.getbuffer())

    return {"status": "success", "file_path": filepath}

# Helper function
def _dict_to_table(data_dict, styles):
    if not isinstance(data_dict, dict):
        return Paragraph("No data available", styles["BodyText"])
    
    data = [[
        Paragraph("<b>" + k.replace('_', ' ').title() + "</b>", styles["BodyText"]),
        Paragraph(str(v), styles["BodyText"])
    ] for k, v in data_dict.items()]

    table = Table(data, colWidths=[200, 300], hAlign="LEFT")
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke)
    ]))
    return table
