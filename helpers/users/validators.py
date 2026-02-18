import re

def validate_password(password: str):
    """
    Valida senha com regras:
    1. mínimo 6 caracteres
    2. máximo 128 caracteres
    3. pelo menos 1 número
    4. pelo menos 1 caractere especial
    5. pelo menos 1 letra maiúscula
    6. pelo menos 1 letra minúscula
    """

    if len(password) < 6:
        return False, "A senha deve ter no mínimo 6 caracteres."
    if len(password) > 128:
        return False, "A senha deve ter no máximo 128 caracteres."
    if not re.search(r"[0-9]", password):
        return False, "A senha deve conter pelo menos um número."
    if not re.search(r"[A-Z]", password):
        return False, "A senha deve conter pelo menos uma letra maiúscula."
    if not re.search(r"[a-z]", password):
        return False, "A senha deve conter pelo menos uma letra minúscula."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=/\\\[\];']", password):
        return False, "A senha deve conter pelo menos um caractere especial."

    return True, "OK"


def validate_email_domain(email: str):
    allowed_domains = [
        "@gruposese.com",
        "@volkswagen.com.br"
    ]

    if any(email.endswith(domain) for domain in allowed_domains):
        return True, "OK"

    return False, "O e-mail deve ser do domínio @gruposese.com ou @volkswagen.com.br."