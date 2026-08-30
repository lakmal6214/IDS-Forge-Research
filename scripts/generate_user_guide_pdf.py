"""
scripts/generate_user_guide_pdf.py
Generates a professional PDF User Guide for IDS Forge:
"User_Guide_How_To_Run_IDS_Forge.pdf"
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to add 'Page X of Y' and header/footer"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#64748b"))

        # Running Header (Pages 2+)
        if self._pageNumber > 1:
            self.drawString(54, 750, "IDS Forge ⚒️ — System Access & Execution Guide")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)

        # Running Footer (All pages)
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 45, 558, 45)
        self.drawString(54, 30, "KIU University — BSc (Hons) Computer Networks & Cyber Security")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 30, page_str)

        self.restoreState()


def build_user_guide_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#2563eb"),
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=12,
        spaceAfter=8,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#334155"),
        spaceAfter=8
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#0f172a"),
        backColor=colors.HexColor("#f1f5f9"),
        borderColor=colors.HexColor("#cbd5e1"),
        borderWidth=0.5,
        borderPadding=6,
        spaceBefore=4,
        spaceAfter=8
    )

    story = []

    # Title Header
    story.append(Paragraph("IDS Forge ⚒️ — System Access & Execution Guide", title_style))
    story.append(Paragraph("Machine Learning-Based Hybrid Intrusion Detection System for IoT Networks", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2563eb"), spaceAfter=12))

    # Metadata Table
    meta_data = [
        [Paragraph("<b>Author:</b>", body_style), Paragraph("R.M.L.S.B. Wijerathna (ID: 14519)", body_style),
         Paragraph("<b>Module:</b>", body_style), Paragraph("COM4901 Final Year Project", body_style)],
        [Paragraph("<b>Degree:</b>", body_style), Paragraph("BSc (Hons) Computer Networks & Cyber Security", body_style),
         Paragraph("<b>Supervisor:</b>", body_style), Paragraph("Mr. Sahan Weerasinghe", body_style)],
        [Paragraph("<b>Institution:</b>", body_style), Paragraph("KIU University, Sri Lanka", body_style),
         Paragraph("<b>GitHub:</b>", body_style), Paragraph("<a href='https://github.com/lakmal6214/IDS-Forge-Research' color='#2563eb'>lakmal6214/IDS-Forge-Research</a>", body_style)]
    ]
    t_meta = Table(meta_data, colWidths=[80, 170, 80, 174])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#f1f5f9")),
        ('PADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 14))

    # Section 1: Quick Start (1-Minute Launch)
    story.append(Paragraph("1. Quick Start (Running on Your Local Machine)", h1_style))
    story.append(Paragraph("To launch the IDS Web Dashboard immediately on your machine, open <b>Command Prompt</b> or <b>PowerShell</b> in the project root folder and run:", body_style))
    story.append(Paragraph("python -m streamlit run app.py", code_style))
    story.append(Paragraph("Your browser will automatically open: <b><a href='http://localhost:8501' color='#2563eb'>http://localhost:8501</a></b>", body_style))
    story.append(Spacer(1, 10))

    # Section 2: Complete Setup Guide for Supervisors / Reviewers
    story.append(Paragraph("2. Full Installation & Setup Guide (For Supervisors / Reviewers)", h1_style))
    story.append(Paragraph("Anyone cloning this repository from GitHub can set up and run the system in 3 simple steps:", body_style))

    story.append(Paragraph("<b>Step 1: Clone the GitHub Repository</b>", body_style))
    story.append(Paragraph("git clone https://github.com/lakmal6214/IDS-Forge-Research.git<br/>cd IDS-Forge-Research", code_style))

    story.append(Paragraph("<b>Step 2: Install Required Dependencies</b>", body_style))
    story.append(Paragraph("python -m pip install -r requirements.txt<br/><i>(Or: py -m pip install -r requirements.txt)</i>", code_style))

    story.append(Paragraph("<b>Step 3: Launch Option A — Interactive Web Dashboard</b>", body_style))
    story.append(Paragraph("python -m streamlit run app.py", code_style))
    story.append(Paragraph("Access the interactive UI in browser at <code>http://localhost:8501</code>.", body_style))

    story.append(Paragraph("<b>Step 4: Launch Option B — Terminal Experimental Pipeline</b>", body_style))
    story.append(Paragraph("python main.py", code_style))
    story.append(Paragraph("Executes all 8 experimental stages (data loading, feature selection, signature matching, ML classifier training, zero-day simulation, and plot rendering).", body_style))

    story.append(Spacer(1, 10))

    # Section 3: Clean Repository Architecture
    story.append(Paragraph("3. Professional Repository Architecture", h1_style))
    story.append(Paragraph("The codebase is structured following industry-standard Python package design:", body_style))

    arch_data = [
        [Paragraph("<b>Directory / File</b>", body_style), Paragraph("<b>Description & Purpose</b>", body_style)],
        [Paragraph("<code>app.py</code>", body_style), Paragraph("Interactive Streamlit Web UI Dashboard entrypoint.", body_style)],
        [Paragraph("<code>main.py</code>", body_style), Paragraph("CLI Experimental Pipeline Orchestrator (Stages 1-8).", body_style)],
        [Paragraph("<code>src/</code>", body_style), Paragraph("Core engine source package (data loader, feature selection, signatures, ML models, hybrid IDS, evaluator, visualizer).", body_style)],
        [Paragraph("<code>docs/</code>", body_style), Paragraph("Complete submission deliverables (Dissertation, Viva Presentation, PDF Report, Technical Guides).", body_style)],
        [Paragraph("<code>scripts/</code>", body_style), Paragraph("Utility generators for Word, PowerPoint, and PDF documentation.", body_style)],
        [Paragraph("<code>output/</code>", body_style), Paragraph("Generated publication figures (Figures 1-8) and CSV benchmark results.", body_style)]
    ]
    t_arch = Table(arch_data, colWidths=[120, 384])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0f172a")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('PADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_arch)

    story.append(Spacer(1, 12))

    # Section 4: Deliverables Index
    story.append(Paragraph("4. Academic Deliverables & Documents Index", h1_style))
    story.append(Paragraph("All academic artifacts located in <code>docs/</code>:", body_style))

    deliv_data = [
        [Paragraph("<b>Document File</b>", body_style), Paragraph("<b>Format</b>", body_style), Paragraph("<b>Description</b>", body_style)],
        [Paragraph("<code>Dissertation_IDS_Forge.docx</code>", body_style), Paragraph("MS Word", body_style), Paragraph("Complete 8,000-10,000 word dissertation.", body_style)],
        [Paragraph("<code>Viva_Presentation_IDS_Forge.pptx</code>", body_style), Paragraph("PPTX", body_style), Paragraph("35-slide deck with speaker notes.", body_style)],
        [Paragraph("<code>Final_Report_IDS_Forge.pdf</code>", body_style), Paragraph("PDF", body_style), Paragraph("Final submission report PDF.", body_style)],
        [Paragraph("<code>User_Guide_How_To_Run_IDS_Forge.pdf</code>", body_style), Paragraph("PDF", body_style), Paragraph("System access & step-by-step execution guide.", body_style)],
        [Paragraph("<code>Technical_Documentation.md</code>", body_style), Paragraph("Markdown", body_style), Paragraph("Architecture & edge gateway deployment guide.", body_style)],
        [Paragraph("<code>Submission_Checklist.md</code>", body_style), Paragraph("Markdown", body_style), Paragraph("COM4901 submission checklist.", body_style)]
    ]
    t_deliv = Table(deliv_data, colWidths=[180, 70, 254])
    t_deliv.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e293b")),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('PADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_deliv)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[+] User Guide PDF generated successfully at: {output_path}")

if __name__ == '__main__':
    out_file = os.path.join("docs", "User_Guide_How_To_Run_IDS_Forge.pdf")
    os.makedirs("docs", exist_ok=True)
    build_user_guide_pdf(out_file)
