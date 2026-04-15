from typing import List, Union

from pydantic import PostgresDsn, RedisDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    database_url: PostgresDsn
    redis_url: RedisDsn
    app_host: str = "localhost"
    app_port: int = 5049
    app_reload: bool = False
    allow_origins: Union[str, List[str]]
    auth_token_secret_key: str
    auth_token_algorithm: str

    @field_validator("allow_origins", mode="before")
    @classmethod
    def assemble_allow_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


config = Config()
