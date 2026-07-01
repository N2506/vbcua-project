import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf_report(topic, metrics, transcript, evaluation, chart_path, output_filename="reports/evaluation_report.pdf"):
    """
    Compiles speech analytics, transcript details, and semantic evaluation data 
    into a structured PDF summary file.
    """
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    
    doc = SimpleDocTemplate(output_filename, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=22, 
        leading=26, textColor=colors.HexColor('#1f77b4'), spaceAfter=15
    )
    section_style = ParagraphStyle(
        'SectionHeading', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=14, 
        leading=18, textColor=colors.HexColor('#2c3e50'), spaceBefore=12, spaceAfter=8
    )
    body_style = ParagraphStyle(
        'BodyTextCustom', parent=styles['BodyText'], fontName='Helvetica', fontSize=10, 
        leading=14, textColor=colors.HexColor('#333333')
    )
    
    story.append(Paragraph("Voice-Based Concept Understanding Analyser (VBCUA)", title_style))
    story.append(Paragraph(f"<b>Target Concept Topic:</b> {topic}", body_style))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("1. Fluency & Acoustic Performance Metrics", section_style))
    data = [
        ['Metric Category', 'Measured Value'],
        ['Total Speech Duration', f"{metrics.get('duration_sec', 0)} seconds"],
        ['Silence / Pause Ratio', f"{int(metrics.get('pause_ratio', 0) * 100)}%"],
        ['Acoustic Energy Density (RMS)', f"{metrics.get('rms_energy', 0)}"]
    ]
    t = Table(data, colWidths=[250, 200])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (1,0), colors.HexColor('#1f77b4')),
        ('TEXTCOLOR', (0,0), (1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#f8f9fa'), colors.white]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("2. Automated Speech Transcription", section_style))
    story.append(Paragraph(transcript if transcript else "No text recorded.", body_style))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("3. Semantic Concept Analysis Evaluation", section_style))
    score = evaluation.get("score", 0.0)
    level = evaluation.get("level", "N/A")
    feedback = evaluation.get("feedback", "N/A")
    
    story.append(Paragraph(f"<b>Semantic Match Score:</b> {score}%", body_style))
    story.append(Paragraph(f"<b>Comprehension Classification:</b> {level}", body_style))
    story.append(Paragraph(f"<b>AI Insight Assessment:</b> {feedback}", body_style))
    story.append(Spacer(1, 15))
    
    if chart_path and os.path.exists(chart_path):
        story.append(Paragraph("4. Speech Amplitude Signal Waveform", section_style))
        story.append(Image(chart_path, width=450, height=135))
        
    doc.build(story)
    return output_filename
