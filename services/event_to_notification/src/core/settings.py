__all__ = ['get_settings', 'KafkaTaskSettings']

from functools import lru_cache

from typing import Callable

from pydantic import BaseModel, BaseSettings

from core.yaml_loader import yaml_settings_source


class KafkaTaskSettings(BaseModel):
    bootstrap_servers: str
    auto_offset_reset: str
    enable_auto_commit: str
    group_id: str
    topics: list[str]


class TaskSettings(BaseModel):
    title: str
    handler: Callable

    class Config:
        arbitrary_types_allowed = True


class Settings(BaseSettings):
    auth_api_url: str = 'http://localhost/auth/'
    notification_api_url = 'http://localhost/api/v1/send/email'
    auth_login: str
    auth_password: str
    backoff_timeout: int = 30
    kafka: KafkaTaskSettings
    cycles_delay: int
    tasks: list[TaskSettings]

    class Config:
        env_nested_delimiter = '__'

        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            """Переопределение старшинства источников настроек."""
            return (
                init_settings,
                env_settings,
                yaml_settings_source,
                file_secret_settings,
            )


@lru_cache
def get_settings():
    settings = Settings()
    return settings



