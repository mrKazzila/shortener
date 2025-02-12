import logging
from functools import lru_cache
from pathlib import Path
from sys import exit
from typing import Annotated, Literal, cast

from annotated_types import Ge, Le, MinLen
from pydantic import HttpUrl, PostgresDsn, RedisDsn, SecretStr, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ("settings",)

logger = logging.getLogger(__name__)


class ProjectBaseSettings(BaseSettings):
    __ROOT_DIR_ID: int = 2

    model_config = SettingsConfigDict(
        env_file=Path(__file__)
        .resolve()
        .parents[__ROOT_DIR_ID]
        .joinpath("env/.env"),
    )


class SentrySettings(ProjectBaseSettings):
    """Settings for Sentry."""

    SENTRY_URL: HttpUrl
    TRACES_SAMPLE_RATE: float
    PROFILES_SAMPLE_RATE: float


class RedisSettings(ProjectBaseSettings):
    """Settings for Redis."""

    REDIS_VERSION: str

    REDIS_HOST: str
    REDIS_PORT: Annotated[int, Ge(1), Le(65_535)]
    REDIS_CACHE_TIME: Annotated[int, Ge(1)]

    @property
    def redis_url(self) -> RedisDsn:
        scheme_ = "redis"
        return RedisDsn.build(
            scheme=scheme_,
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
        )


class DatabaseSettings(ProjectBaseSettings):
    """Settings for DB."""

    POSTGRES_VERSION: str

    DB_PROTOCOL: str
    DB_HOST: str
    DB_PORT: cast(str, Annotated[int, Ge(1), Le(65_535)])
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: Annotated[SecretStr, MinLen(8)]

    @property
    def dsn(self, protocol=None) -> PostgresDsn:
        protocol = protocol or self.DB_PROTOCOL

        return PostgresDsn.build(
            scheme=protocol,
            username=self.DB_USER,
            password=self.DB_PASSWORD.get_secret_value(),
            host=self.DB_HOST,
            port=self.DB_PORT,
            path=f"{self.DB_NAME}",
        )


class Settings(ProjectBaseSettings):
    """Main settings for project."""

    POSTGRES_VERSION: str

    DB_PROTOCOL: str
    DB_HOST: str
    DB_PORT: cast(str, Annotated[int, Ge(1), Le(65_535)])
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: Annotated[SecretStr, MinLen(8)]

    @property
    def dsn(self, protocol=None) -> PostgresDsn:
        protocol = protocol or self.DB_PROTOCOL

        return PostgresDsn.build(
            scheme=protocol,
            username=self.DB_USER,
            password=self.DB_PASSWORD.get_secret_value(),
            host=self.DB_HOST,
            port=self.DB_PORT,
            path=f"{self.DB_NAME}",
        )

    APP_NAME: str
    MODE: Literal["TEST", "DEV", "PROD"]

    BASE_URL: str
    DOMAIN: str
    DOMAIN_PORT: Annotated[int, Ge(1), Le(65_535)]

    KEY_LENGTH: Annotated[int, Ge(3), Le(10)]


@lru_cache
def settings() -> Settings:
    logger.info("Loading settings from env")

    try:
        return Settings()

    except ValidationError as error_:
        logger.error("Error at loading settings from env. %s", error_)
        exit(str(error_))
