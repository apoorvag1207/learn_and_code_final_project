import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

class EmailSender:
    def __init__(self):
        self.smtp_host = os.getenv("SMTP_HOST")
        self.smtp_port = int(os.getenv("SMTP_PORT", 587))
        self.smtp_user = os.getenv("SMTP_USER")
        self.smtp_pass = os.getenv("SMTP_PASSWORD")

    def send_email(self, to_email, subject, body):
        try:
            message = MIMEMultipart()
            message['From'] = self.smtp_user
            message['To'] = to_email
            message['Subject'] = subject

            message.attach(MIMEText(body, 'plain'))

            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_pass)
                server.send_message(message)

            print(f"[EmailSender] Email sent to {to_email}")
        except Exception as e:
            print(f"[EmailSender] Failed to send email: {e}")
