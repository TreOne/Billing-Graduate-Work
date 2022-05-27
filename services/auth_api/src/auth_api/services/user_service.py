from http.client import CONFLICT, BAD_REQUEST

import pyotp

from auth_api.exceptions import UserServiceException
from auth_api.extensions import db
from auth_api.models.user import Role, User, AuthHistory


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
            return {'msg': 'The user does not have this role.'}, CONFLICT

        db.session.add(user)
        db.session.commit()

        return user.roles

    def get_roles(self, user_uuid: str):
        user = User.query.get_or_404(user_uuid)
        return user.roles

    def get_auth_history(self, user_uuid: str):
        auth_history = AuthHistory.query.filter_by(user_uuid=user_uuid)
        return auth_history

    def change_user_totp_status(self, user_uuid: str, totp_request):

        user = User.query.filter_by(uuid=user_uuid).first()

        totp_status = totp_request.get('totp_status')
        totp_code = totp_request.get('totp_code')

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
