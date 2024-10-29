import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from fastapi import APIRouter, BackgroundTasks

from config import conf

auth_router = APIRouter()


def send_email_smtp(recipient_email: str, subject: str, message: str):
    msg = MIMEMultipart()
    msg["From"] = conf.smtp.SMTP_USERNAME
    msg["To"] = recipient_email
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "plain"))

    try:
        with smtplib.SMTP(conf.smtp.SMTP_SERVER, conf.smtp.SMTP_PORT) as server:
            server.starttls()
            server.login(conf.smtp.SMTP_USERNAME, conf.smtp.SMTP_PASSWORD)
            server.sendmail(conf.smtp.SMTP_USERNAME, recipient_email, msg.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")


@auth_router.get("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email_smtp, email, "Notification", "Hello")
    return {"message": "Notification sent in the background"}
