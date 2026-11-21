
from password_validator import validar_senha

senhas = [
    "123456",
    "Ab1!kQ9#",
    "C0mplex@Pass#2026"
]

for senha in senhas:
    resultado = validar_senha(senha)

    print("-" * 45)
    print("Senha:", senha)
    print("Válida:", resultado.is_valid)
    print("Força:", resultado.forca)
    print("Mensagens:", resultado.mensagens)
