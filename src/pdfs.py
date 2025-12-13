from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

class Pdfs:
    def __init__(self):
        self.pdf=SimpleDocTemplate("report.pdf", pagesize=A4)
        self.elements=[]
        self.styles = getSampleStyleSheet()

    def create_pdf(self):
        self.elements=self.createContent()
        self.pdf.build(self.elements)

    def createContent(self):
        self.elements.append(Paragraph(
            "<b>Daily Productivity Report</b>",
            self.styles["Title"]
        ))
        self.elements.append(Spacer(1, 15))

        self.elements.append(Paragraph(
            "This report contains tasks, analysis, and visual graphs.",
            self.styles["Normal"]
        ))
        self.elements.append(Spacer(1, 20))

        self.elements.append(Image("graph.png", width=400, height=250))
        self.elements.append(Spacer(1, 20))

        return self.elements

        
