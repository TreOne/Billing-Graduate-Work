__all__ = ['render_template', 'shorten_url', 'send_message']

import os

import bitly_api
import requests
from jinja2 import Environment, FileSystemLoader, select_autoescape

from core.settings import get_settings

settings = get_settings()


def render_template(data: dict, template_name: str) -> str:
    env = Environment(
        loader=FileSystemLoader(os.path.join('/', 'src/templates')),
        autoescape=select_autoescape(['html', 'xml']),
    )
    template = env.get_template(template_name)
    rendered = template.render(data)
    return rendered


def shorten_url(url: str) -> str:
    access = bitly_api.Connection(access_token=settings.bitly_access_token)
    short_url = access.shorten(url)
    return short_url['url']


def send_message(url: str, message: dict[str, any]) -> dict[str, any]:
    response = requests.post(url, json=message)
    return response.json()
