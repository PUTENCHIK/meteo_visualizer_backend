from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    database_url: PostgresDsn
    redis_url: RedisDsn
    app_host: str = "localhost"
    app_port: int = 5049
    app_reload: bool = False
    auth_token_secret_key: str
    auth_token_algorithm: str

    model_config = SettingsConfigDict(env_file=".env")


config = Config()
