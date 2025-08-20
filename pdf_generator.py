import os
import tempfile
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import HexColor

def generate_pdf_report(report_data: dict) -> str:
    """Generate a PDF report from the report data"""
    
    # Create temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    temp_file.close()
    
    # Create PDF document
    doc = SimpleDocTemplate(
        temp_file.name,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=HexColor('#2c3e50')
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        spaceBefore=20,
        textColor=HexColor('#34495e')
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=12,
        alignment=TA_JUSTIFY,
        leading=14
    )
    
    list_style = ParagraphStyle(
        'CustomList',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6,
        leftIndent=20,
        bulletIndent=10
    )
    
    # Build content
    content = []
    
    # Title page
    content.append(Paragraph(report_data.get('report_title', 'Financial Report'), title_style))
    content.append(Spacer(1, 20))
    
    # Company info
    company_name = report_data.get('company_name', 'Company')
    executive_name = report_data.get('executive_name', 'Executive')
    
    content.append(Paragraph(f"<b>Company:</b> {company_name}", body_style))
    content.append(Paragraph(f"<b>Prepared for:</b> {executive_name}", body_style))
    content.append(Paragraph(f"<b>Date:</b> {datetime.now().strftime('%B %d, %Y')}", body_style))
    content.append(Spacer(1, 30))
    
    # Financial summary
    if 'revenue' in report_data:
        content.append(Paragraph("Financial Overview", heading_style))
        content.append(Paragraph(f"<b>Revenue:</b> ₹{report_data['revenue']:,.2f}", body_style))
        content.append(Paragraph(f"<b>Profit:</b> ₹{report_data['profit']:,.2f}", body_style))
        content.append(Paragraph(f"<b>Growth:</b> {report_data['growth_percentage']}%", body_style))
        content.append(Spacer(1, 20))
    
    # Executive Summary
    if 'executive_summary' in report_data:
        content.append(Paragraph("Executive Summary", heading_style))
        summary_text = report_data['executive_summary'].replace('\n', '<br/>')
        content.append(Paragraph(summary_text, body_style))
        content.append(Spacer(1, 15))
    
    # Key Trends
    if 'key_trends' in report_data:
        content.append(Paragraph("Key Trends Analysis", heading_style))
        trends_text = report_data['key_trends'].replace('\n', '<br/>')
        content.append(Paragraph(trends_text, body_style))
        content.append(Spacer(1, 15))
    
    # Top 3 Risks
    if 'top_risks' in report_data and report_data['top_risks']:
        content.append(Paragraph("Top 3 Critical Risks", heading_style))
        risks = report_data['top_risks']
        if isinstance(risks, list):
            for i, risk in enumerate(risks[:3], 1):
                content.append(Paragraph(f"{i}. {risk}", list_style))
        else:
            content.append(Paragraph(str(risks), body_style))
        content.append(Spacer(1, 15))
    
    # Risk Assessment
    if 'risks' in report_data:
        content.append(Paragraph("Risk Assessment", heading_style))
        risks_text = report_data['risks'].replace('\n', '<br/>')
        content.append(Paragraph(risks_text, body_style))
        content.append(Spacer(1, 15))
    
    # Top 3 Recommendations
    if 'top_recommendations' in report_data and report_data['top_recommendations']:
        content.append(Paragraph("Top 3 Priority Recommendations", heading_style))
        recommendations = report_data['top_recommendations']
        if isinstance(recommendations, list):
            for i, rec in enumerate(recommendations[:3], 1):
                content.append(Paragraph(f"{i}. {rec}", list_style))
        else:
            content.append(Paragraph(str(recommendations), body_style))
        content.append(Spacer(1, 15))
    
    # Strategic Recommendations
    if 'recommendations' in report_data:
        content.append(Paragraph("Strategic Recommendations", heading_style))
        rec_text = report_data['recommendations'].replace('\n', '<br/>')
        content.append(Paragraph(rec_text, body_style))
    
    # Build PDF
    doc.build(content)
    
    return temp_file.name
