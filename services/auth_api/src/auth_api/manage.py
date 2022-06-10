import json
import os

import click
from flask.cli import with_appcontext
from sqlalchemy import or_

from auth_api.database import session
from auth_api.models import User
from auth_api.models.user import Role


@click.command()
@click.option(
    '--username', '-u', help='Superuser name.',
)
@click.option(
    '--email', '-e', help='Superuser email.',
)
@click.option(
    '--password', '-p', help='Superuser password.',
)
@with_appcontext
def createsuperuser(username, email, password):
    """Создание суперпользователя."""

    if username is None:
        username = os.getenv('AUTHAPI_SUPERUSER_NAME')
    if email is None:
        email = os.getenv('AUTHAPI_SUPERUSER_EMAIL')
    if password is None:
        password = os.getenv('AUTHAPI_SUPERUSER_PASSWORD')

    new_superuser = User(
        username=username, email=email, password=password, is_active=True, is_superuser=True,
    )

    existing_superuser = session.query(User).filter(
        or_(User.username == new_superuser.username, User.email == new_superuser.email),
    ).first()

    if existing_superuser:
        click.echo(f'{new_superuser.username} ({new_superuser.email}) already created!')
        return
    session.add(new_superuser)
    session.commit()
    click.echo('Superuser created!')


@click.command()
@with_appcontext
def loaddata():
    """Инициализация базы данных."""
    dirname = os.path.dirname(__file__)
    contract_roles_filename = os.path.join(dirname, 'settings/contract_roles.json')
    with open(contract_roles_filename) as f:
        roles = json.load(f)
    for role in roles:
        existing_role = session.query(Role).get(role['uuid'])
        if existing_role:
            click.echo(f'{existing_role.name} already created!')
            continue
        session.add(Role(name=role['code'], uuid=role['uuid']))
    session.commit()
    click.echo(f'Load roles: {len(roles)}')

    contract_admins_filename = os.path.join(dirname, 'settings/contract_admins.json')
    role_admin = session.query(Role).get("c45ea0ef-f9b4-4569-af09-9ee7b0a9c16c")
    with open(contract_admins_filename) as f:
        admins = json.load(f)
    for admin in admins:
        username = admin['login']
        password = os.getenv(f'{username.upper()}_PASSWORD')
        existing_admin = session.query(User).filter(User.username == username).first()
        if existing_admin:
            click.echo(f'{existing_admin.username} already created!')
            continue
        new_admin = User(username=username, password=password)
        session.add(new_admin)
        new_admin.roles.append(role_admin)
    session.commit()
    click.echo(f'Load admins: {len(admins)}')
