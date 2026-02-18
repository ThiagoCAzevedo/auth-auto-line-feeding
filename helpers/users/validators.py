import re

class UserValidators:
    def validate_password(self, password: str):
        if len(password) < 6:
            return False, "The password must contain minimum of 6 characters."
        if len(password) > 128:
            return False, "The password must contain maximum of 128 characters."
        if not re.search(r"[0-9]", password):
            return False, "The password must contain a number."
        if not re.search(r"[A-Z]", password):
            return False, "The password must contain a upper case character."
        if not re.search(r"[a-z]", password):
            return False, "The password must contain a lower case character."
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=/\\\[\];']", password):
            return False, "The password must contain a special character."

        return True, "Password created succesfully"

    def validate_email_domain(self, email: str):
        allowed_domains = [
            "@gruposese.com",
            "@volkswagen.com.br"
        ]

        if any(email.endswith(domain) for domain in allowed_domains):
            return True, "E-mail created successfully"

        return False, "The e-mail must be of @gruposese.com or @volkswagen.com.br domain."