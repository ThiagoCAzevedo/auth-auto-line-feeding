import re
from common.exceptions import HTTPExceptions


class UserValidators:
    @staticmethod
    def validate_password(password: str):
        if len(password) < 6:
            raise HTTPExceptions.http_400("A senha deve conter no mínimo 6 caracteres.")  
        if len(password) > 128:
            raise HTTPExceptions.http_400("A senha deve conter no máximo 128 caracteres.")
        if not re.search(r"[0-9]", password):
            raise HTTPExceptions.http_400("A senha deve conter um número.")
        if not re.search(r"[A-Z]", password):
            raise HTTPExceptions.http_400("A senha deve conter um caractere maiúsculo.")
        if not re.search(r"[a-z]", password):
            raise HTTPExceptions.http_400("A senha deve conter um caractere minúsculo.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=/\\\[\];']", password):
            raise HTTPExceptions.http_400("A senha deve conter um caractere especial.")

    @staticmethod
    def validate_email_domain(email: str):
        allowed_domains = [
            "@gruposese.com",
            "@volkswagen.com.br"
        ]

        if not any(email.endswith(domain) for domain in allowed_domains):
            raise HTTPExceptions.http_400("O e-mail deve ser do domínio @gruposese.com ou @volkswagen.com.br.")
