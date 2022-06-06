from http.client import CONFLICT, BAD_REQUEST, NOT_FOUND
from typing import Optional

import pyotp
from sqlalchemy import or_

from auth_api.api.v1.schemas.user import UserSchema
from auth_api.commons.jwt_utils import get_user_uuid_from_token, deactivate_access_token, create_extended_access_token, \
    deactivate_all_refresh_tokens
from auth_api.commons.pagination import paginate
from auth_api.database import session
from auth_api.models.user import User, AuthHistory


class UserServiceException(Exception):
    def __init__(self, message, http_code=None):
        super().__init__(message)
        self.http_code = http_code


class UserService:

    def get_auth_history(self, user_uuid: str):
        auth_history = session.query(AuthHistory).filter_by(user_uuid=user_uuid).order_by(
            AuthHistory.created_at.desc())
        return auth_history

    def change_user_totp_status(self, user_uuid, totp_status: bool, totp_code: str):

        user = session.query(User).filter_by(uuid=user_uuid).first()

        if totp_status == user.is_totp_enabled:
            raise UserServiceException('This status has already been established.', http_code=CONFLICT)

        secret = user.two_factor_secret
        totp = pyotp.TOTP(secret)

        if not totp.verify(totp_code):
            raise UserServiceException('Wrong totp code.', http_code=BAD_REQUEST)

        user.is_totp_enabled = totp_status
        session.commit()

        return totp_status

    def get_user_totp_link(self, user_uuid: str):
        user = session.query(User).filter_by(uuid=user_uuid).first()
        if user.two_factor_secret is None:
            secret = pyotp.random_base32()
            user.two_factor_secret = secret
            session.commit()
        else:
            secret = user.two_factor_secret

        totp = pyotp.TOTP(secret)
        provisioning_url = totp.provisioning_uri(name=user.username, issuer_name='PractixMovie')
        return provisioning_url

    def update_current_user(self, access_token, email: Optional[str] = None, username: Optional[str] = None, password: Optional[
        str] = None):

        user_uuid = get_user_uuid_from_token(access_token)
        schema = UserSchema(partial=True)
        user = session.query(User).get(user_uuid)
        if not user:
            raise UserServiceException('User not found.', http_code=NOT_FOUND)
        if email:
            user.email = email
        if username:
            user.username = username
        if password:
            user.password = password

        session.commit()

        deactivate_access_token(access_token)
        refresh_uuid = access_token['refresh_uuid']
        new_access_token = create_extended_access_token(user_uuid, refresh_uuid)
        return schema.dump(user), new_access_token

    def delete_current_user(self, access_token):
        user_uuid = get_user_uuid_from_token(access_token)
        user = session.query(User).get(user_uuid)
        user.is_active = False
        session.commit()

        deactivate_access_token(access_token)
        deactivate_all_refresh_tokens(user_uuid)

    def get_user(self, user_uuid):
        schema = UserSchema()
        user = session.query(User).get(user_uuid)
        if not user:
            raise UserServiceException('User not found.', http_code=NOT_FOUND)
        return {'user': schema.dump(user)}

    def update_user(self, user_uuid, email: Optional[str] = None, username: Optional[str] = None, password: Optional[
        str] = None):
        schema = UserSchema(partial=True)
        user = session.query(User).get(user_uuid)
        if not user:
            raise UserServiceException('User not found.', http_code=NOT_FOUND)
        if email:
            user.email = email
        if username:
            user.username = username
        if password:
            user.password = password

        session.commit()
        return schema.dump(user)

    def delete_user(self, user_uuid):
        user = session.query(User).get(user_uuid)
        if not user:
            raise UserServiceException('User not found.', http_code=NOT_FOUND)
        if not user.is_active:
            raise UserServiceException('The user is already blocked.', http_code=CONFLICT)

        user.is_active = False
        session.commit()

        deactivate_all_refresh_tokens(user_uuid)

    def get_users_list(self):
        schema = UserSchema(many=True)
        query = session.query(User).filter_by(is_active=True)
        return paginate(query, schema)

    def create_user(self, email: str, username: str, password: str):
        schema = UserSchema()
        existing_user = session.query(User).filter(
            or_(User.username == username, User.email == email),
        ).first()
        if existing_user:
            raise UserServiceException('Username or email is already taken!', http_code=CONFLICT)
        user = User(username=username, email=email, password=password)
        session.add(user)
        session.commit()
        return schema.dump(user)
