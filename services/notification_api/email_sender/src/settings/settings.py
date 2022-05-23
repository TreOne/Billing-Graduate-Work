from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, BaseSettings


class RabbitmqSettings(BaseModel):
    user: str
    password: str
    host: str
    port: int


class RedisSettings(BaseModel):
    host: str
    port: int


class EmailServiceSettings(BaseModel):
    daily_limit: int
    urgent_reserve: int


class Settings(BaseSettings):
    """Настройки приложения."""

    rabbitmq: RabbitmqSettings
    redis: RedisSettings
    email: EmailServiceSettings

    class Config:
        env_nested_delimiter = '__'
        case_sensitive = False

        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            """Переопределение старшинства источников настроек."""
            return (
                init_settings,
                env_settings,
                yaml_settings_source,
                file_secret_settings,
            )


def yaml_settings_source(settings: BaseSettings) -> dict[str, Any]:
    """Возвращает настройки из файла settings.yaml."""
    settings_path = Path(__file__).parent / 'settings.yaml'
    with settings_path.open('r', encoding='utf-8') as f:
        yaml_settings = yaml.load(f, Loader=yaml.Loader)
    return yaml_settings


@lru_cache
def get_settings() -> Settings:
    """Синглтон для бедных."""
    return Settings()
