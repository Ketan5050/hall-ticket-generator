# Hall Ticket Generator 🎟️

This Python-based application generates hall tickets from an Excel file and sends them via email.

## Features 🚀
- Reads student details from an Excel file.
- Generates personalized hall tickets in PDF format.
- Adds profile photos, barcodes, and signatures.
- Sends hall tickets via email.
- User-friendly GUI for uploading files.

## Installation 🔧
1. **Clone this repository:**
   ```sh
   git clone https://github.com/your-username/hall-ticket-generator.git
   cd hall-ticket-generator
2. **Install dependencies:**  
   ```sh
   pip install -r requirements.txt
4. **Set up environment variables:**  
   - Create a .env file in the project root.
   - Add your email credentials:
    ```sh  
   EMAIL_ADDRESS=your-email@gmail.com  
   EMAIL_PASSWORD=your-app-password

5. **Run the application:**  
    ```sh
   python hall_ticket_generator.py

6. **Usage:**  
   - Upload an Excel file with student details.  
   - The system will generate hall tickets and email them automatically.  
   - Check the log window for progress.

7. **File Structure:**
    ```sh  
   hall-ticket-generator/  
   │-- hall_ticket_generator.py   # Main script  
   │-- requirements.txt           # Dependencies  
   │-- .gitignore                 # Git ignore rules  
   │-- README.md                  # Documentation  
   │-- profile_pictures/          # Store student profile images  
   │-- signatures/                # Store principal signature  
   │-- hall_tickets/              # Generated PDF hall tickets  

8. **Dependencies:**  
   - pandas  
   - barcode  
   - reportlab  
   - tkinter  
   - smtplib  
   - dotenv  
   ```sh
   Install them using:  
   pip install -r requirements.txt  

9. **License**:  
   This project is licensed under the MIT License.
