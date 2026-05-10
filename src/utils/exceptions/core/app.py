from pathlib import Path

from src.utils.exceptions.core.base import AppException


class RedisClientUnavailableException(AppException):
    def __init__(self):
        super().__init__(
            "Не удалось подключиться к Redis. Убедитесь, что служба запущена"
        )


class InitialDataFileNotExistException(AppException):
    def __init__(self, path: Path):
        super().__init__(f"Файл данных инициализации '{path}' не существует")


class InitialDataFileWrongSuffixException(AppException):
    def __init__(self, path: Path):
        super().__init__(
            f"Файл данных инициализации '{path}' имеет неверное расширение, "
            "ожидалось: '.yaml', '.yml'"
        )
