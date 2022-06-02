__all__ = ['settings', 'KafkaTaskSettings']

from functools import lru_cache
from pathlib import Path
from typing import Any, List, Type

import yaml
from pydantic import BaseModel, BaseSettings

from services.event_to_notification.models.abc_data_stucture import TransferClass


class KafkaTaskSettings(BaseModel):
    bootstrap_servers: str
    auto_offset_reset: str
    enable_auto_commit: str
    group_id: str
    topics: List[str]


class TaskSettings(BaseModel):
    task_name: str

    class Config:
        arbitrary_types_allowed = True


class Settings(BaseSettings):
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


def yaml_settings_source(settings: BaseSettings) -> dict[str, Any]:
    """Возвращает настройки из файла settings.yaml."""
    settings_path = Path(__file__).parent / 'settings.yaml'
    with settings_path.open('r', encoding='utf-8') as f:
        yaml_settings = yaml.load(f, Loader=yaml.Loader)
    return yaml_settings


settings = Settings()