from src.utils.exceptions.base import AppException


class RedisClientUnavailableException(AppException):
    def __init__(self):
        super().__init__(
            "Не удалось подключиться к Redis. Убедитесь, что служба запущена"
        )
