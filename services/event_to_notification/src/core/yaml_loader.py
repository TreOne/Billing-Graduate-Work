from pathlib import Path

import yaml
from pydantic import BaseSettings


def func_loader(loader, node):
    """A loader for functions."""
    params = loader.construct_mapping(node)
    module = __import__(params["module"], fromlist=[params["name"]])
    return getattr(module, params["name"])


def get_loader():
    """Return a yaml loader."""
    loader = yaml.Loader
    loader.add_constructor("!Func", func_loader)
    return loader


def yaml_settings_source(settings: BaseSettings) -> dict[str, any]:
    """Возвращает настройки из файла settings.yaml."""
    settings_path = Path(__file__).parent / 'settings.yaml'
    with settings_path.open('r', encoding='utf-8') as f:
        yaml_settings = yaml.load(f, Loader=get_loader())
    return yaml_settings
