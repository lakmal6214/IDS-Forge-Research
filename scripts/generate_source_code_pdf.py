"""
scripts/generate_source_code_pdf.py
Generates a complete, publication-grade PDF document containing the entire source code 
of the IDS Forge project for KIU COM4901 Final Year Individual Project submission.
Output: docs/Source_Code_IDS_Forge_14519.pdf
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Skip cover page

        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#475569"))
        
        # Header
        self.drawString(54, 750, "IDS Forge ⚒️  |  Complete Source Code Appendix")
        self.setFont("Helvetica", 8)
        self.drawRightString(612 - 54, 750, "KIU COM4901 Final Year Individual Project")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 744, 612 - 54, 744)

        # Footer
        self.line(54, 48, 612 - 54, 48)
        self.setFont("Helvetica", 8)
        self.drawString(54, 34, "Student: R.M.L.S.B. Wijerathna (ID: 14519)  |  BSc (Hons) Computer Networks & Cyber Security")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(612 - 54, 34, page_text)
        self.restoreState()


def build_source_code_pdf(output_pdf_path):
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor("#0F172A"),
        alignment=1, # Center
        spaceAfter=12
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#2563EB"),
        alignment=1,
        spaceAfter=24
    )

    meta_label_style = ParagraphStyle(
        'MetaLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#1E293B")
    )

    meta_val_style = ParagraphStyle(
        'MetaValue',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#334155")
    )

    file_title_style = ParagraphStyle(
        'FileTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#FFFFFF")
    )

    file_desc_style = ParagraphStyle(
        'FileDesc',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#94A3B8")
    )

    code_line_style = ParagraphStyle(
        'CodeLine',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#0F172A")
    )

    code_num_style = ParagraphStyle(
        'CodeNum',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#64748B"),
        alignment=2 # Right
    )

    h1_style = ParagraphStyle(
        'Heading1Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=14,
        spaceAfter=8
    )

    story = []

    # ---------------------------------------------------------
    # COVER PAGE
    # ---------------------------------------------------------
    story.append(Spacer(1, 20))
    story.append(Paragraph("KIU UNIVERSITY, SRI LANKA", ParagraphStyle('Inst', fontName='Helvetica-Bold', fontSize=13, leading=16, alignment=1, textColor=colors.HexColor("#1E293B"))))
    story.append(Paragraph("FACULTY OF COMPUTER SCIENCE AND ENGINEERING", subtitle_style))
    story.append(Spacer(1, 15))

    story.append(Paragraph("IDS FORGE ⚒️", title_style))
    story.append(Paragraph("COMPLETE SOURCE CODE DOCUMENTATION APPENDIX", ParagraphStyle('Sub', fontName='Helvetica-Bold', fontSize=14, leading=18, alignment=1, textColor=colors.HexColor("#1E3A8A"))))
    story.append(Spacer(1, 10))
    story.append(Paragraph("A Machine Learning-Based Hybrid Intrusion Detection System for IoT Networks", ParagraphStyle('Desc', fontName='Helvetica-Oblique', fontSize=11, leading=15, alignment=1, textColor=colors.HexColor("#475569"))))
    
    story.append(Spacer(1, 30))

    # Metadata Card Table
    meta_data = [
        [Paragraph("Student Name:", meta_label_style), Paragraph("R.M.L.S.B. Wijerathna", meta_val_style)],
        [Paragraph("Student Registration ID:", meta_label_style), Paragraph("14519", meta_val_style)],
        [Paragraph("Degree Program:", meta_label_style), Paragraph("BSc (Hons) in Computer Networks and Cyber Security", meta_val_style)],
        [Paragraph("Module Code & Title:", meta_label_style), Paragraph("COM4901 - Final Year Individual Project", meta_val_style)],
        [Paragraph("Project Supervisor:", meta_label_style), Paragraph("Mr. Sahan Weerasinghe", meta_val_style)],
        [Paragraph("GitHub Repository:", meta_label_style), Paragraph("https://github.com/lakmal6214/IDS-Forge-Research", meta_val_style)],
        [Paragraph("Submission Date:", meta_label_style), Paragraph("31 August 2026", meta_val_style)],
    ]
    t_meta = Table(meta_data, colWidths=[2.2*inch, 4.3*inch])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#E2E8F0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#F1F5F9")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_meta)

    story.append(Spacer(1, 40))
    story.append(Paragraph("This document contains the complete, unedited source code implementation of the IDS Forge software pipeline, including data loader utilities, 3-stage feature selection algorithms, Phase 1 signature engine, Phase 2 machine learning models, sequential hybrid coordinator, evaluation routines, visualizer tools, and web UI application.", ParagraphStyle('Note', fontName='Helvetica', fontSize=9.5, leading=14, alignment=0, textColor=colors.HexColor("#64748B"))))

    story.append(PageBreak())

    # ---------------------------------------------------------
    # SOURCE CODE DIRECTORY INDEX
    # ---------------------------------------------------------
    story.append(Paragraph("SOURCE CODE FILE INDEX", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0F172A"), spaceAfter=14))

    code_files = [
        ("app.py", "IDS Forge Streamlit Interactive Web Application Dashboard", "Main UI Web App"),
        ("main.py", "CLI Pipeline Orchestrator (Stages 1 through 8)", "CLI Pipeline Entry"),
        ("src/__init__.py", "Package Initializer & System Path Registration", "Core Package"),
        ("src/data_loader.py", "Dataset Preprocessing, Cleansing, & Synthetic BoT-IoT Synthesis", "Data Engine"),
        ("src/feature_selection.py", "3-Stage Feature Selection (Pearson Correlation, Mutual Info, RFE)", "Feature Pipeline"),
        ("src/signature_engine.py", "Phase 1 Deterministic Signature Engine (9 Protocol Rules)", "Phase 1 Engine"),
        ("src/ml_models.py", "Phase 2 Machine Learning Classifiers (DT, RF, Gradient Boosting)", "Phase 2 Engine"),
        ("src/hybrid_ids.py", "Two-Tier Sequential Hybrid Engine Coordination Architecture", "Hybrid Coordinator"),
        ("src/evaluator.py", "Classification Benchmark & Hardware Overhead Evaluator (psutil)", "Hardware Evaluator"),
        ("src/visualizer.py", "High-Resolution Publication Plot & Diagram Generator", "Graphics Engine"),
        ("run_ids_forge.bat", "Automated 1-Click Launcher Script for Windows Operating Systems", "Windows Launcher"),
        ("requirements.txt", "Python Dependency Specification Package Requirements", "Dependencies")
    ]

    idx_data = [[Paragraph("File Path", ParagraphStyle('IH', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white)),
                 Paragraph("Module Category", ParagraphStyle('IH', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white)),
                 Paragraph("Description & Operational Scope", ParagraphStyle('IH', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white))]]

    for f_path, f_desc, f_cat in code_files:
        idx_data.append([
            Paragraph(f_path, ParagraphStyle('IFP', fontName='Courier-Bold', fontSize=9, textColor=colors.HexColor("#1E3A8A"))),
            Paragraph(f_cat, ParagraphStyle('IFC', fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor("#475569"))),
            Paragraph(f_desc, ParagraphStyle('IFD', fontName='Helvetica', fontSize=9, textColor=colors.HexColor("#334155")))
        ])

    t_idx = Table(idx_data, colWidths=[2.1*inch, 1.4*inch, 3.0*inch])
    t_idx.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E293B")),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_idx)
    story.append(Spacer(1, 20))
    story.append(PageBreak())

    # ---------------------------------------------------------
    # PRINT SOURCE CODE FILES
    # ---------------------------------------------------------
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    for f_rel, f_desc, f_cat in code_files:
        full_path = os.path.join(base_dir, f_rel.replace('/', os.sep))
        if not os.path.exists(full_path):
            print(f"[!] Warning: File {full_path} not found. Skipping.")
            continue

        with open(full_path, 'r', encoding='utf-8', errors='ignore') as fp:
            file_content = fp.read()

        lines = file_content.splitlines()
        line_count = len(lines)

        # Header Card for File
        hdr_table_data = [
            [
                Paragraph(f"📄 {f_rel}", file_title_style),
                Paragraph(f"Category: {f_cat}  |  Total Lines: {line_count}", ParagraphStyle('FHRight', fontName='Helvetica-Bold', fontSize=9, alignment=2, textColor=colors.HexColor("#94A3B8")))
            ],
            [
                Paragraph(f"Description: {f_desc}", file_desc_style),
                Paragraph(f"Path: {f_rel}", ParagraphStyle('FHPath', fontName='Courier', fontSize=8, alignment=2, textColor=colors.HexColor("#CBD5E1")))
            ]
        ]
        t_fhdr = Table(hdr_table_data, colWidths=[4.2*inch, 2.3*inch])
        t_fhdr.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#1E293B")),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ]))
        
        story.append(t_fhdr)
        story.append(Spacer(1, 6))

        # Format Code Lines into Table with Line Numbers
        code_table_data = []
        for l_num, line_str in enumerate(lines, 1):
            # Escape HTML characters for ReportLab Paragraph
            safe_line = (
                line_str.replace('&', '&amp;')
                        .replace('<', '&lt;')
                        .replace('>', '&gt;')
                        .replace(' ', '&nbsp;')
                        .replace('\t', '&nbsp;&nbsp;&nbsp;&nbsp;')
            )
            if not safe_line:
                safe_line = '&nbsp;'

            code_table_data.append([
                Paragraph(str(l_num), code_num_style),
                Paragraph(safe_line, code_line_style)
            ])

        t_code = Table(code_table_data, colWidths=[0.45*inch, 6.05*inch])
        t_code.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.HexColor("#F1F5F9")),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('TOPPADDING', (0,0), (-1,-1), 1.2),
            ('BOTTOMPADDING', (0,0), (-1,-1), 1.2),
            ('LEFTPADDING', (0,0), (-1,-1), 4),
            ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ]))

        story.append(t_code)
        story.append(Spacer(1, 18))
        story.append(PageBreak())

    # Build PDF Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[+] Source Code PDF generated successfully at: {output_pdf_path}")


if __name__ == '__main__':
    out_pdf = os.path.join("docs", "Source_Code_IDS_Forge_14519.pdf")
    os.makedirs("docs", exist_ok=True)
    build_source_code_pdf(out_pdf)
