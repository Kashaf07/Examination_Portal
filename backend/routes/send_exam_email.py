from flask import Blueprint, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import MySQLdb.cursors

def create_send_email_routes(mysql):
    send_email_bp = Blueprint('send_email', __name__)

    @send_email_bp.route('/api/send_exam_emails', methods=['POST'])
    def send_exam_emails():
        data = request.get_json()
        exam = data.get("exam", {})
        applicants = data.get("applicants", [])

        try:
            sender_email = "examinationportal2025@gmail.com"
            sender_password = "zwdp rwro piku dwib"
            subject = f"Exam Assignment: {exam['Exam_Name']}"

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            for applicant in applicants:
                email = applicant.get("Email")

                # Fetch full applicant data from DB by email
                cursor.execute("SELECT Full_Name, Email, Password FROM applicants WHERE Email = %s", (email,))
                db_applicant = cursor.fetchone()

                if not db_applicant:
                    print(f"⚠️ Applicant with email {email} not found.")
                    continue

                full_name = db_applicant['Full_Name']
                receiver_email = db_applicant['Email']
                password = db_applicant['Password']

                # 🔗 LOGIN PAGE LINK (Update this when you deploy to production)
                # For localhost: http://localhost:5173
                # For production: https://yourdomain.com
                login_link = "http://localhost:5173"  # 👈 Change this to your production URL later

                # 📧 EMAIL BODY WITH LOGIN LINK
                body = f"""Dear {full_name},

You have been assigned the following exam:

========================================
EXAM DETAILS
========================================

Exam ID: {exam['Exam_Id']}
Exam Name: {exam['Exam_Name']}
Date: {exam['Exam_Date']}
Time: {exam['Exam_Time']}

========================================
YOUR LOGIN CREDENTIALS
========================================

Email: {receiver_email}
Password: {password}

========================================
LOGIN TO YOUR EXAM FROM THIS LINK
========================================

{login_link}

IMPORTANT INSTRUCTIONS:
1. Login using the credentials provided above
2. Enter the Exam ID when prompted
3. Read all instructions carefully before starting
4. Do NOT refresh the page during the exam
5. Do NOT switch tabs or windows during the exam
6. Ensure stable internet connection

========================================

Good luck with your exam!

Best regards,
Examination Management Cell
"""

                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = receiver_email
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'plain', 'utf-8'))

                # Send email
                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.starttls()
                    server.login(sender_email, sender_password)
                    server.sendmail(sender_email, receiver_email, msg.as_string())

            return jsonify({'success': True, 'message': 'Emails sent successfully!'})

        except Exception as e:
            print("❌ Email sending error:", e)
            return jsonify({'success': False, 'message': f'Failed to send emails: {str(e)}'}), 500

    return send_email_bp