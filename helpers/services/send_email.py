import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os


load_dotenv("config/.env")


class EmailService:
    SMTP_HOST = os.getenv("SMTP_HOST")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    SMTP_USER = os.getenv("SMTP_USER")
    SMTP_PASS = os.getenv("SMTP_PASS")

    APP_VERIFY_URL = os.getenv("APP_VERIFY_EMAIL")
    APP_RESET_URL = os.getenv("APP_RESET_PASSWORD")

    @classmethod
    def _send(cls, to_email: str, subject: str, body: str):
        try:
            msg = MIMEText(body, "plain", "utf-8")
            msg["Subject"] = subject
            msg["From"] = cls.SMTP_USER
            msg["To"] = to_email

            with smtplib.SMTP(cls.SMTP_HOST, cls.SMTP_PORT, timeout=10) as server:
                server.starttls()
                server.login(cls.SMTP_USER, cls.SMTP_PASS)
                server.send_message(msg)

        except Exception as e:
            print(f"[EmailService] Erro ao enviar email: {e}")
            raise Exception("Falha ao enviar o e-mail.")

    @classmethod
    def send_verification_email(cls, to_email: str, token: str):
        link = f"{cls.APP_VERIFY_URL}?token={token}"

        body = (
            "Olá!\n\n"
            "Obrigado por criar sua conta.\n\n"
            "Clique no link abaixo para verificar seu e-mail:\n"
            f"{link}\n\n"
            "Se você não criou esta conta, ignore este e-mail."
        )

        cls._send(to_email, "Verifique seu e-mail", body)

    @classmethod
    def send_password_reset_email(cls, to_email: str, token: str):
        link = f"{cls.APP_RESET_URL}?token={token}"

        body = (
            "Olá!\n\n"
            "Recebemos um pedido para redefinir sua senha.\n\n"
            "Clique no link abaixo para criar uma nova senha:\n"
            f"{link}\n\n"
            "Este link expira em 30 minutos."
        )

        cls._send(to_email, "Redefinição de senha", body)