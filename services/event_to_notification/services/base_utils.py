__all__ = ["render_template", "shorten_url", "get_data"]

import os
from urllib.parse import urljoin

import bitly_api
import requests
from jinja2 import Environment, FileSystemLoader, select_autoescape

from core.settings import settings


def render_template(data: dict, template_name: str) -> str:
    env = Environment(
        loader=FileSystemLoader(os.path.join("/", "src/templates")),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template(template_name)
    rendered = template.render(data)
    return rendered


def shorten_url(url: str) -> str:
    access = bitly_api.Connection(access_token=settings.bitly_access_token)
    short_url = access.shorten(url)
    return short_url["url"]


def get_data(url: str, user_id: str) -> dict[str, any]:
    response = requests.get(urljoin(url, user_id))
    return response.json()
