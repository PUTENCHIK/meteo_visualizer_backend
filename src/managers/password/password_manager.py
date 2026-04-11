from pwdlib import PasswordHash

from src.utils import SingletonMetaclass


class PasswordManager(metaclass=SingletonMetaclass):
    """
    Менеджер-сингтон для создания и валидации паролей
    """

    SECRET_KEY = "4a3288191dcbb53728f0f56e3b41ab69da3415dc7879d1117efc82dab1193e27"
    ALGORITHM = "HS256"

    password_hash = PasswordHash.recommended()

    def __init__(self):
        pass

    def verify_password(self, password: str, hashed: str) -> bool:
        return self.password_hash.verify(password, hashed)

    def hash_password(self, password: str) -> str:
        return self.password_hash.hash(password)
