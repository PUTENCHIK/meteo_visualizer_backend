from pathlib import Path
from uuid import UUID

import yaml

from src.config import config
from src.schemas import InitialDataSchema
from src.utils import SingletonMetaclass
from src.utils.exceptions import (
    InitialDataFileNotExistException,
    InitialDataFileWrongSuffixException,
)


class InitialDataManager(metaclass=SingletonMetaclass):
    """
    Менеджер-сингтон для синхронизации данных инициализации с базой данных
    """

    __initial_data: InitialDataSchema
    __base_role_id: UUID

    @property
    def initial_data(self) -> InitialDataSchema:
        return self.__initial_data

    @property
    def base_role_id(self) -> UUID:
        return self.__base_role_id

    @base_role_id.setter
    def base_role_id(self, value: UUID):
        self.__base_role_id = value

    def __init__(self):
        self.__initial_data = self._get_initial_data(config.initial_data_path)

    def _get_initial_data(self, path: str) -> InitialDataSchema:
        fpath = Path(path).absolute()
        if not fpath.exists():
            raise InitialDataFileNotExistException(fpath)
        if fpath.suffix not in [".yaml", ".yml"]:
            raise InitialDataFileWrongSuffixException(fpath)

        with open(fpath, encoding="utf-8") as file:
            data = yaml.safe_load(file)
            return InitialDataSchema(**data)
