import os

from jinja2 import Environment, FileSystemLoader


def render_template(template_name: str, data: dict) -> str:
    template_path = os.path.join(os.path.dirname(__file__), 'templates')
    env = Environment(loader=FileSystemLoader(template_path))
    template = env.get_template(template_name + '.html')
    rendered = template.render(data)
    return rendered
