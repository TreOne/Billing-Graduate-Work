from http.client import CONFLICT, BAD_REQUEST

import pyotp

from auth_api.extensions import db
from auth_api.models.user import Role, User, AuthHistory


class UserServiceException(Exception):
    def __init__(self, message, http_code=None):
        super().__init__(message)
        self.http_code = http_code


class UserService:

    def add_role(self, user_uuid: str, role_uuid: str):
        user = User.query.get_or_404(user_uuid)
        role = Role.query.get_or_404(role_uuid)
        user.roles.append(role)

        db.session.add(user)
        db.session.commit()

        return user.roles

    def remove_role(self, user_uuid: str, role_uuid: str):
        user = User.query.get_or_404(user_uuid)
        role = Role.query.get_or_404(role_uuid)

        if role in user.roles:
            user.roles.remove(role)
        else:
            raise UserServiceException('The user does not have this role.', http_code=CONFLICT)

        db.session.add(user)
        db.session.commit()

        return user.roles

    def get_roles(self, user_uuid: str):
        user = User.query.get_or_404(user_uuid)
        return user.roles

    def get_auth_history(self, user_uuid: str):
        auth_history = AuthHistory.query.filter_by(user_uuid=user_uuid)
        return auth_history

    def change_user_totp_status(self, user_uuid,  totp_status: bool, totp_code: str):

        user = User.query.filter_by(uuid=user_uuid).first()

        if totp_status == user.is_totp_enabled:
            raise UserServiceException('This status has already been established.', http_code=CONFLICT)

        secret = user.two_factor_secret
        totp = pyotp.TOTP(secret)

        if not totp.verify(totp_code):
            raise UserServiceException('Wrong totp code.', http_code=BAD_REQUEST)

        user.is_totp_enabled = totp_status
        db.session.commit()

        return totp_status

    def get_user_totp_link(self, user_uuid: str):
        user = User.query.filter_by(uuid=user_uuid).first()
        if user.two_factor_secret is None:
            secret = pyotp.random_base32()
            user.two_factor_secret = secret
            db.session.commit()
        else:
            secret = user.two_factor_secret

        totp = pyotp.TOTP(secret)
        provisioning_url = totp.provisioning_uri(name=user.username, issuer_name='PractixMovie')
        return provisioning_url
