from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Table, TableStyle
import os

def ReportGenerate(patient_data):
    # Create a temporary file for the PDF report
    pdf_file_path = os.path.join(os.path.expanduser("~"), "/home/imap/pandas/MINE/MedLab/Downloads", f"{patient_data['name']} Pathology Report.pdf")
    
    # Create a canvas
    c = canvas.Canvas(pdf_file_path, pagesize=letter)
    width, height = letter
    
    # Helper function to draw a bordered section
    def draw_bordered_section(title, y_start, content_func):
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
    contact_text = "Contact: info@lancetlabs.com | Phone: +(256) 756-7890 | Address: 123 Clinic Rd, Mukono, Uganda"
    contact_width = c.stringWidth(contact_text, "Helvetica", 12)
    c.drawString((width - contact_width) / 2, height - 50, contact_text)
    
    # Patient Information
    def draw_patient_info(y):
        c.setFont("Helvetica", 12)
        c.drawString(60, y, f"Name: {patient_data['name']}")
        c.drawString(60, y - 20, f"Phone: {patient_data['phone']}")
        c.drawString(60, y - 40, f"Gender: {patient_data['gender']}")
        c.drawString(60, y - 60, f"Date of Birth: {patient_data['dob']}")
        c.drawString(60, y - 80, f"Age: {patient_data['age']}")
        c.drawString(60, y - 100, f"Address: {patient_data['address']}")
        c.drawString(60, y - 120, f"Medical History: {patient_data['medical_history']}")
    
    y = draw_bordered_section("Patient Information", height - 80, draw_patient_info)
    
    # Tests and Results
    def draw_tests_results(y):
        styles = getSampleStyleSheet()
        data = [["Test", "Description", "Result", "Date", "Comment"]]
        for test_data, result in patient_data['tests']:
            data.append([
                test_data['test_name'],
                test_data['description'],
                result['status'],
                result['test_date'],
                result['comments']
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
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        table.wrapOn(c, width - 120, height)
        table.drawOn(c, 60, y - 150)
    
    y = draw_bordered_section("Tests and Results", y - 20, draw_tests_results)
    
    # Prescription
    def draw_prescription(y):
        c.setFont("Helvetica", 12)
        c.drawString(60, y, "Medical Prescription:")
        c.line(60, y - 20, width - 60, y - 20)
        c.line(60, y - 40, width - 60, y - 40)
        c.line(60, y - 60, width - 60, y - 60)
        c.line(60, y - 80, width - 60, y - 80)
        c.line(60, y - 100, width - 60, y - 100)
        c.line(60, y - 120, width - 60, y - 120)
    
    draw_bordered_section("Prescription", y - 20, draw_prescription)
    
    # Save the PDF
    c.save()
    return pdf_file_path