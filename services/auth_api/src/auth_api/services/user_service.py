from http.client import CONFLICT, BAD_REQUEST

import pyotp
from sqlalchemy import or_

from auth_api.api.v1.schemas.user import UserSchema
from auth_api.commons.jwt_utils import get_user_uuid_from_token, deactivate_access_token, create_extended_access_token, \
    deactivate_all_refresh_tokens
from auth_api.commons.pagination import paginate
from auth_api.extensions import db
from auth_api.models.user import User, AuthHistory


class UserServiceException(Exception):
    def __init__(self, message, http_code=None):
        super().__init__(message)
        self.http_code = http_code


class UserService:

    def get_auth_history(self, user_uuid: str):
        auth_history = AuthHistory.query.filter_by(user_uuid=user_uuid)
        return auth_history

    def change_user_totp_status(self, user_uuid, totp_status: bool, totp_code: str):

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

    def update_current_user(self, access_token, user_data):

        user_uuid = get_user_uuid_from_token(access_token)
        schema = UserSchema(partial=True)
        user = User.query.get_or_404(user_uuid)
        user = schema.load(user_data, instance=user)

        db.session.commit()

        deactivate_access_token(access_token)
        refresh_uuid = access_token['refresh_uuid']
        new_access_token = create_extended_access_token(user_uuid, refresh_uuid)
        return schema.dump(user), new_access_token

    def delete_current_user(self, access_token):
        user_uuid = get_user_uuid_from_token(access_token)
        user = User.query.get(user_uuid)
        user.is_active = False
        db.session.commit()

        deactivate_access_token(access_token)
        deactivate_all_refresh_tokens(user_uuid)

    def get_user(self, user_uuid):
        schema = UserSchema()
        user = User.query.get_or_404(user_uuid)
        return {'user': schema.dump(user)}

    def update_user(self, user_uuid, user_data):

        schema = UserSchema(partial=True)
        user = User.query.get_or_404(user_uuid)
        user = schema.load(user_data, instance=user)

        db.session.commit()
        return schema.dump(user)

    def delete_user(self, user_uuid):
        user = User.query.get_or_404(user_uuid)
        if not user.is_active:
            raise UserServiceException('The user is already blocked.', http_code=CONFLICT)

        user.is_active = False
        db.session.commit()

        deactivate_all_refresh_tokens(user_uuid)

    def get_users_list(self):
        schema = UserSchema(many=True)
        query = User.query.filter_by(is_active=True)
        return paginate(query, schema)

    def create_user(self, user_data):
        schema = UserSchema()
        user = schema.load(user_data)

        existing_user = User.query.filter(
            or_(User.username == user.username, User.email == user.email),
        ).first()
        if existing_user:
            raise UserServiceException('Username or email is already taken!', http_code=CONFLICT)

        db.session.add(user)
        db.session.commit()
        return schema.dump(user)
