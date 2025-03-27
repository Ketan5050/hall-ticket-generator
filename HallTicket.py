import os
import pandas as pd
from barcode import Code128
from barcode.writer import ImageWriter
from tkinter import Tk, Label, Button, filedialog, messagebox, Text, Scrollbar, END
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv 

# Load environment variables from .env file
load_dotenv()

# Paths for input and output
OUTPUT_DIR = "hall_tickets"
os.makedirs(OUTPUT_DIR, exist_ok=True)

PROFILE_PICTURES_DIR = "profile_pictures"  # Update with correct path
SIGNATURE_PATH = "signatures/principal_signature.jpg"  # Update with correct path

# Email configuration (Use environment variables for security)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_email_with_attachment(to_email, subject, body, attachment_path, log_widget):
    try:
        msg = EmailMessage()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(body)

        # Attach the PDF file
        with open(attachment_path, "rb") as file:
            pdf_data = file.read()
            msg.add_attachment(pdf_data, maintype="application", subtype="pdf", filename=os.path.basename(attachment_path))

        # Connect to SMTP server and send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
            log_widget.insert(END, f"Email sent to {to_email}\n")
    except Exception as e:
        log_widget.insert(END, f"Failed to send email to {to_email}: {e}\n")

def generate_barcode(student_id, output_path):
    barcode = Code128(student_id, writer=ImageWriter())
    barcode.save(output_path.split(".")[0])

def create_hall_ticket(student, output_path, log_widget):
    pdf = canvas.Canvas(output_path, pagesize=landscape(A4))
    pdf.setFont("Helvetica", 12)

    width, height = landscape(A4)
    margin = 50

    pdf.setFont("Helvetica-Bold", 26)
    pdf.drawCentredString(width / 2, height - margin, "College Name")
    
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawCentredString(width / 2, height - margin - 30, "Hall Ticket")

    photo_path = os.path.join(PROFILE_PICTURES_DIR, f"{student['Unique ID']}.jpg")
    photo_x = width - margin - 120
    photo_y = height - margin - 140
    photo_width = 100
    photo_height = 120
    if os.path.exists(photo_path):
        pdf.drawImage(photo_path, photo_x, photo_y, width=photo_width, height=photo_height)
    else:
        pdf.rect(photo_x, photo_y, photo_width, photo_height, stroke=1, fill=0)
        pdf.drawString(photo_x + 10, photo_y + 50, "Photo Missing")

    barcode_path = os.path.join(OUTPUT_DIR, f"{student['Unique ID']}_barcode.png")
    generate_barcode(student["Unique ID"], barcode_path)
    barcode_x = photo_x + (photo_width - 150) / 2
    barcode_y = photo_y - 70
    pdf.drawImage(barcode_path, barcode_x, barcode_y, width=150, height=50)

    pdf.setFont("Helvetica", 18)
    details = [
        f"Candidate Name: {student['Candidate Name']}",
        f"Mother Name: {student['Mother Name']}",
        f"Seat No: {student['Seat No']}",
        f"Email: {student['Email']}",
    ]
    details_y = height - margin - 100
    line_spacing = 30
    for detail in details:
        pdf.drawString(margin, details_y, detail)
        details_y -= line_spacing

    timetable = [
        "Timetable:",
        "Subject 1: Date & Time",
        "Subject 2: Date & Time",
    ]
    timetable_y = details_y - 40
    for entry in timetable:
        pdf.drawString(margin, timetable_y, entry)
        timetable_y -= line_spacing

    pdf.setFont("Helvetica", 16)
    signature_x = width - 220
    signature_y = margin + 150
    if os.path.exists(SIGNATURE_PATH):
        pdf.drawImage(SIGNATURE_PATH, signature_x, signature_y - 40, width=150, height=50)
    pdf.drawString(signature_x, signature_y + 20, "Principal's Signature")

    pdf.save()
    log_widget.insert(END, f"Hall ticket created: {output_path}\n")
    if os.path.exists(barcode_path):
        os.remove(barcode_path)

def process_file(file_path, log_widget):
    try:
        students = pd.read_excel(file_path)
    except Exception as e:
        log_widget.insert(END, f"Error reading the file: {e}\n")
        return

    for _, student in students.iterrows():
        output_path = os.path.join(OUTPUT_DIR, f"{student['Unique ID']}_hall_ticket.pdf")
        create_hall_ticket(student, output_path, log_widget)
        email_body = f"Dear {student['Candidate Name']},\n\nPlease find attached your hall ticket.\n\nBest regards,\nCollege Name"
        send_email_with_attachment(student["Email"], "Your Hall Ticket", email_body, output_path, log_widget)

    messagebox.showinfo("Process Complete", "All hall tickets have been created & emailed successfully!")

def upload_file(log_widget):
    file_path = filedialog.askopenfilename(title="Select Excel File", filetypes=[["Excel files", "*.xlsx *.xls"]])
    if file_path:
        process_file(file_path, log_widget)

def main():
    root = Tk()
    root.title("Hall Ticket Generator")
    root.geometry("600x400")

    label = Label(root, text="Upload an Excel file to generate hall tickets")
    label.pack(pady=10)

    upload_button = Button(root, text="Upload Excel File", command=lambda: upload_file(log_widget))
    upload_button.pack(pady=5)

    log_widget = Text(root, wrap="word", height=15, width=70)
    log_widget.pack(pady=10)

    scrollbar = Scrollbar(root, command=log_widget.yview)
    log_widget.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    root.mainloop()

if __name__ == "__main__":
    main()
