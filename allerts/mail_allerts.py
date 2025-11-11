from email.message import EmailMessage
from config import google_settings
import smtplib

smtp_user = google_settings.smtp_user
smtp_password = google_settings.smtp_password
to_addrs = [google_settings.recipient_one, google_settings.recipient_two]

def send_email(subject: str, body: str):
    if not smtp_user or not smtp_password:
        raise RuntimeError("SMTP credentials not set. Please set environment variables.")

    msg = EmailMessage()
    msg["From"] = smtp_user
    msg["To"] = ", ".join(to_addrs)
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(smtp_user, smtp_password)
        smtp.send_message(msg)

if __name__ == "__main__":
    send_email(
        subject="🔔 Test Notification from IBKR Alert System",
        body="היי! זו הודעת בדיקה ממערכת ההתראות שלך 😊",
    )
    print("Email sent successfully!")