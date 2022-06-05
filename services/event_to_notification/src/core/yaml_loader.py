from pathlib import Path

import yaml
from pydantic import BaseSettings


def yaml_settings_source(settings: BaseSettings) -> dict[str, any]:
    """Loads settings from settings.yaml."""
    settings_path = Path(__file__).parent / 'settings.yaml'
    with settings_path.open('r', encoding='utf-8') as f:
        yaml_settings = yaml.load(f, Loader=yaml.Loader)
    return yaml_settings
