from functools import lru_cache
from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel, BaseSettings


class KafkaSettings(BaseModel):
    bootstrap_servers: str
    auto_offset_reset: str
    enable_auto_commit: str
    group_id: str
    topics: Optional[list[str]]


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


def yaml_settings_source(settings: BaseSettings) -> dict[str, any]:
    """Возвращает настройки из файла settings.yaml."""
    settings_path = Path(__file__).parent / 'settings.yaml'
    with settings_path.open('r', encoding='utf-8') as f:
        yaml_settings = yaml.load(f, Loader=yaml.Loader)
    return yaml_settings

@lru_cache
def get_settings():
    settings = Settings()
    return settings
