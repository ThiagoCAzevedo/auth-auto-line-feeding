import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv("config/.env")

def send_verification_email(to_email: str, token: str):
    verification_link = f'{os.getenv("APP_VERIFY_EMAIL")}?token={token}'
    
    subject = "Verifique seu e-mail"
    body = f"""
    Olá!

    Obrigado por criar sua conta.
    
    Clique no link abaixo para verificar seu e-mail:
    {verification_link}

    Se você não criou esta conta, ignore este e-mail.
    """

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = os.getenv("SMTP_USER")
    msg["To"] = to_email

    with smtplib.SMTP(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT"))) as server:
        server.starttls()
        server.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))
        server.send_message(msg)


def send_password_reset_email(to_email: str, token: str):
    reset_link = f"{os.getenv('APP_RESET_PASSWORD')}?token={token}"

    body = f"""
    Olá!

    Recebemos um pedido para redefinir sua senha.
    Clique no link abaixo para criar uma nova senha:
    {reset_link}

    Este link expira em 30 minutos.
    """

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = "Redefinição de senha"
    msg["From"] = os.getenv("SMTP_USER")
    msg["To"] = to_email

    with smtplib.SMTP(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT"))) as server:
        server.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))
        server.send_message(msg)