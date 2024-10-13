from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.utils import simpleSplit
import os

def ReportGenerate(patient_data):
    pdf_file_path = os.path.join(os.path.expanduser("~"), "pandas/MINE/MedLab/Downloads", f"{patient_data['name']} Pathology Report.pdf")
    
    c = canvas.Canvas(pdf_file_path, pagesize=letter)
    width, height = letter

    def check_space_needed(required_space):
        """ Check if there is enough space on the current page, otherwise create a new page. """
        nonlocal y
        if y - required_space < 60:  # 60 is a margin threshold before the bottom
            c.showPage()  # Start a new page
            y = height - 30  # Reset y-coordinate for the new page

    def draw_bordered_section(title, y_start, content_func):
        """ Draw a bordered section with a title and dynamic content. """
        check_space_needed(200)  # Check for space before drawing

        c.setStrokeColor(colors.black)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(60, y_start, title)
        c.rect(50, y_start - 180, width - 100, 200)
        content_func(y_start - 20)
        return y_start - 200
    
    # Logo and contact details
    c.setFont("Helvetica-Bold", 16)
    logo_text = "LANCET LABORATORIES"
    logo_width = c.stringWidth(logo_text, "Helvetica-Bold", 16)
    c.drawString((width - logo_width) / 2, height - 30, logo_text)
    
    c.setFont("Helvetica", 12)
    contact_text = "info@lancetlabs.com | +(256) 756-7890 | 123 Clinic Rd, Mukono, Uganda"
    contact_width = c.stringWidth(contact_text, "Helvetica", 12)
    c.drawString((width - contact_width) / 2, height - 50, contact_text)

    y = height - 80  # Initialize y-coordinate

    def draw_patient_info(y):
        c.setFont("Helvetica", 12)
        info_lines = [
            f"Name: {patient_data['name']}",
            f"Phone: {patient_data['phone']}",
            f"Gender: {patient_data['gender']}",
            f"Date of Birth: {patient_data['dob']}",
            f"Age: {patient_data['age']}",
            f"Address: {patient_data['address']}",
            "Medical History:"
        ]
        
        for line in info_lines:
            check_space_needed(15)  # Check for space for each line
            c.drawString(60, y, line)
            y -= 15
        
        # Wrap and draw medical history
        medical_history = patient_data['medical_history']
        wrapped_text = simpleSplit(medical_history, "Helvetica", 12, width - 130)
        for i, line in enumerate(wrapped_text):
            check_space_needed(15)  # Check for space for each wrapped line
            c.drawString(60, y, line)
            y -= 15
            if i >= 3:  # Limit to 3 lines
                c.drawString(60, y, "...")
                y -= 15
                break

    y = draw_bordered_section("Patient Information", y, draw_patient_info)

    def draw_tests_results(y):
        styles = getSampleStyleSheet()
        custom_style = ParagraphStyle('CustomStyle', parent=styles['Normal'], fontSize=10, leading=12)
        
        data = [["Test", "Status", "Date", "Comment"]]
        for test in patient_data['tests']:
            wrapped_comment = Paragraph(test['comments'], custom_style)
            data.append([
                test['test_name'],
                test['status'],
                test['test_date'],
                wrapped_comment
            ])
        
        table = Table(data, colWidths=[80, 100, 80, 80, 120])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))
        table.wrapOn(c, width - 120, height)
        check_space_needed(150)  # Check for space before drawing the table
        table.drawOn(c, 60, y - 150)

    y = draw_bordered_section("Tests and Results", y, draw_tests_results)

    def draw_prescription(y):
        c.setFont("Helvetica", 12)
        c.drawString(60, y, "Medical Prescription:")
        for i in range(6):
            check_space_needed(20)  # Check for space for each line
            c.line(60, y - 20 * (i + 1), width - 60, y - 20 * (i + 1))
    
    y = draw_bordered_section("Prescription", y, draw_prescription)

    c.save()
    return pdf_file_path
