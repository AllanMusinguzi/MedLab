from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import os

def generate_report(patient_data):
    # Create a temporary file for the PDF report
    pdf_file_path = os.path.join(os.path.expanduser("~"), "Desktop", f"{patient_data['name']}_report.pdf")

    # Create a canvas
    c = canvas.Canvas(pdf_file_path, pagesize=letter)
    width, height = letter

    # Draw outer border
    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    c.rect(50, 50, width - 100, height - 100)

    # Top Box: Logo and Contact Details
    c.setFillColor(colors.lightgrey)
    c.rect(50, height - 50, width - 100, 60, stroke=0, fill=1)

    # Logo Placeholder (You can replace this with an actual logo)
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.black)
    c.drawString(60, height - 30, "Your Clinic Logo")
    c.setFont("Helvetica", 12)
    c.drawString(60, height - 50, "Contact: example@example.com | Phone: (123) 456-7890 | Address: 123 Clinic Rd, City, Country")

    # Second Box: Patient Information
    c.setFillColor(colors.white)
    c.rect(50, height - 110, width - 100, 80, stroke=1, fill=1)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(60, height - 80, "Patient Information")
    
    c.setFont("Helvetica", 12)
    c.drawString(60, height - 100, f"Name: {patient_data['name']}")
    c.drawString(60, height - 120, f"Phone: {patient_data['phone']}")
    c.drawString(60, height - 140, f"Gender: {patient_data['gender']}")
    c.drawString(60, height - 160, f"Date of Birth: {patient_data['dob']}")
    c.drawString(60, height - 180, f"Age: {patient_data['age']}")
    c.drawString(60, height - 200, f"Address: {patient_data['address']}")
    c.drawString(60, height - 220, f"Medical History: {patient_data['medical_history']}")

    # Third Box: Tests and Results
    c.setFillColor(colors.white)
    c.rect(50, height - 240, width - 100, 120, stroke=1, fill=1)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(60, height - 220, "Tests and Results")

    y = height - 240 - 20
    for test_name, result in patient_data['tests']:
        c.setFont("Helvetica", 12)
        c.drawString(60, y, f"Test: {test_name[0]}, Description: {test_name[1]}")
        y -= 20
        c.drawString(80, y, f"Result: {result[0]}, Date: {result[1]}, Comment: {result[2]}")
        y -= 20

    # Fourth Box: Prescription
    c.setFillColor(colors.white)
    c.rect(50, y - 20, width - 100, 80, stroke=1, fill=1)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(60, y, "Prescription")
    c.setFont("Helvetica", 12)
    c.drawString(60, y - 20, "__________________________________________________")
    c.drawString(60, y - 40, "__________________________________________________")

    # Save the PDF
    c.save()

    return pdf_file_path
