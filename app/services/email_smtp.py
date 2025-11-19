import smtplib
from email.mime.text import MIMEText
from app.core.config import get_settings

settings = get_settings()


def send_2fa_email(to_email: str, code: str):
    sender = settings.EMAIL_SENDER
    password = settings.EMAIL_PASSWORD  # contraseña de aplicación Gmail

    msg = MIMEText(f"Your 2FA code is: {code}")
    msg["Subject"] = "Your 2FA Code"
    msg["From"] = sender
    msg["To"] = to_email

    # Gmail SMTP SSL (puerto 465)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, to_email, msg.as_string())
