from functools import lru_cache
from pathlib import Path
from sys import exit
from typing import Annotated, cast

from annotated_types import Ge, Le, MinLen
from pydantic import (
    PostgresDsn,
    RedisDsn,
    SecretStr,
    ValidationError,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


class ProjectBaseSettings(BaseSettings):
    __ROOT_DIR_ID: int = 2
    __env_file = Path(__file__).resolve().parents[__ROOT_DIR_ID].joinpath('env/.env')

    model_config = SettingsConfigDict(
        env_file=__env_file,
    )


class ProjectSettings(ProjectBaseSettings):
    BASE_URL: str

    DOMAIN: str
    DOMAIN_PORT: int

    KEY_LENGTH: Annotated[int, Ge(3), Le(10)]


class DatabaseSettings(ProjectBaseSettings):
    """Settings for SQL DB."""

    DB_PROTOCOL: str = 'postgresql+asyncpg'
    DB_HOST: str
    DB_PORT: cast(str, Annotated[int, Ge(1), Le(65_535)])
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: Annotated[SecretStr, MinLen(8)]

    REDIS_HOST: str
    REDIS_PORT: Annotated[int, Ge(1), Le(65_535)]
    REDIS_CACHE_TIME: Annotated[int, Ge(1)]

    @property
    def redis_url(self) -> RedisDsn:
        scheme_ = 'redis'
        url_ = RedisDsn.build(
            scheme=scheme_,
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
        )

        return str(url_)

    @property
    def dsn(self, protocol=None) -> PostgresDsn:
        protocol = protocol or self.DB_PROTOCOL
        url_ = PostgresDsn.build(
            scheme=protocol,
            username=self.DB_USER,
            password=self.DB_PASSWORD.get_secret_value(),
            host=self.DB_HOST,
            port=self.DB_PORT,
            path=f'{self.DB_NAME}',
        )

        return str(url_)


class Settings(ProjectSettings, DatabaseSettings):
    """Main settings."""


@lru_cache
def settings() -> Settings:
    print('Loading settings from env')

    try:
        settings_ = Settings()
        return settings_

    except ValidationError as e:
        exit(e)
