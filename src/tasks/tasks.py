import smtplib
from email.message import EmailMessage

from celery import Celery
from src.config import SMTP_USER, SMTP_PASSWORD, REDIS_PORT

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

celery = Celery("tasks", broker=f"redis://localhost:{REDIS_PORT}")


def get_email_template_dashboard(username: str):
    email = EmailMessage()
    email["Subject"] = "Some application report"
    email["From"] = SMTP_USER
    email["To"] = SMTP_USER

    email.set_content(
        "<div>"
        f'<h1 style="color: red;">Hello, {username}, there is your report. Check it!</h1>'
        '<img src="https://static.vecteezy.com/system/resources/previews/008/295/031/original/custom-relationship'
        "-management-dashboard-ui-design-template-suitable-designing-application-for-android-and-ios-clean-style-app"
        '-mobile-free-vector.jpg" width="600">'
        "</div>",
        subtype="html",
    )
    return email


def send_email_report_dashboard(username: str):
    email = get_email_template_dashboard(username)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)


@celery.task
def send_email_report_dashboard_with_celery(username: str):
    return send_email_report_dashboard(username)