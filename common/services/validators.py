import re
from common.exceptions import HTTPExceptions


class UserValidators:
    @staticmethod
    def validate_password(password: str):
        if len(password) < 6:
            raise HTTPExceptions.http_400("The password must contain minimum of 6 characters.")  
        if len(password) > 128:
            raise HTTPExceptions.http_400("The password must contain maximum of 128 characters.")
        if not re.search(r"[0-9]", password):
            raise HTTPExceptions.http_400("The password must contain a number.")
        if not re.search(r"[A-Z]", password):
            raise HTTPExceptions.http_400("The password must contain a upper case character.")
        if not re.search(r"[a-z]", password):
            raise HTTPExceptions.http_400("The password must contain a lower case character.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=/\\\[\];']", password):
            raise HTTPExceptions.http_400("The password must contain a special character.")

    @staticmethod
    def validate_email_domain(email: str):
        allowed_domains = [
            "@gruposese.com",
            "@volkswagen.com.br"
        ]

        if not any(email.endswith(domain) for domain in allowed_domains):
            raise HTTPExceptions.http_400("The e-mail must be of @gruposese.com or @volkswagen.com.br domain.")
