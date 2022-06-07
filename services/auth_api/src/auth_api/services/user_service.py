import datetime
from http.client import BAD_REQUEST, CONFLICT, NOT_FOUND
from typing import Optional

import pyotp
from sqlalchemy import or_

from auth_api.api.v1.schemas.user import UserSchema
from auth_api.commons.jwt_utils import (create_extended_access_token, deactivate_access_token,
                                        deactivate_all_refresh_tokens, get_user_uuid_from_token)
from auth_api.commons.pagination import paginate
from auth_api.database import session
from auth_api.extensions import db
from auth_api.models.user import AuthHistory, User, UsersRoles
from auth_api.services.exceptions import ServiceException


class UserServiceException(ServiceException):
    pass


class UserService:
    def get_auth_history(self, user_uuid: str):
        # ToDO тут из-за пагинации оставил flask-alchemy
        auth_history = (
            db.session.query(AuthHistory)
            .filter_by(user_uuid=user_uuid)
            .order_by(AuthHistory.created_at.desc())
        )
        return auth_history

    def change_user_totp_status(self, user_uuid, totp_status: bool, totp_code: str):
        user = session.query(User).get(user_uuid)

        if totp_status == user.is_totp_enabled:
            raise UserServiceException(
                "This status has already been established.", http_code=CONFLICT
            )

        secret = user.two_factor_secret
        totp = pyotp.TOTP(secret)

        if not totp.verify(totp_code):
            raise UserServiceException("Wrong totp code.", http_code=BAD_REQUEST)

        user.is_totp_enabled = totp_status
        session.commit()

        return totp_status

    def get_user_totp_link(self, user_uuid: str):
        user = session.query(User).get(user_uuid)
        if user.two_factor_secret is None:
            secret = pyotp.random_base32()
            user.two_factor_secret = secret
            session.commit()
        else:
            secret = user.two_factor_secret

        totp = pyotp.TOTP(secret)
        provisioning_url = totp.provisioning_uri(
            name=user.username, issuer_name="PractixMovie"
        )
        return provisioning_url

    def update_current_user(
            self,
            access_token,
            email: Optional[str] = None,
            username: Optional[str] = None,
            password: Optional[str] = None,
    ):

        user_uuid = get_user_uuid_from_token(access_token)
        schema = UserSchema()
        user = session.query(User).get(user_uuid)
        if not user:
            raise UserServiceException("User not found.", http_code=NOT_FOUND)
        if email:
            user.email = email
        if username:
            user.username = username
        if password:
            user.password = password

        session.commit()

        deactivate_access_token(access_token)
        refresh_uuid = access_token["refresh_uuid"]
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
            raise UserServiceException("User not found.", http_code=NOT_FOUND)
        return {"user": schema.dump(user)}

    def update_user(
            self,
            user_uuid,
            email: Optional[str] = None,
            username: Optional[str] = None,
            password: Optional[str] = None,
    ):
        schema = UserSchema()
        user = session.query(User).get(user_uuid)
        if not user:
            raise UserServiceException("User not found.", http_code=NOT_FOUND)
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
            raise UserServiceException("User not found.", http_code=NOT_FOUND)
        if not user.is_active:
            raise UserServiceException(
                "The user is already blocked.", http_code=CONFLICT
            )

        user.is_active = False
        session.commit()

        deactivate_all_refresh_tokens(user_uuid)

    def get_users_list(self):
        schema = UserSchema(many=True)
        # ToDO тут из-за пагинации оставил flask-alchemy
        query = db.session.query(User).filter_by(is_active=True)
        return paginate(query, schema)

    def create_user(self, email: str, username: str, password: str):
        schema = UserSchema()
        existing_user = (
            session.query(User)
            .filter(or_(User.username == username, User.email == email), )
            .first()
        )
        if existing_user:
            raise UserServiceException(
                "Username or email is already taken!", http_code=CONFLICT
            )
        user = User(username=username, email=email, password=password)
        session.add(user)
        session.commit()
        return schema.dump(user)

    def get_users_with_ending_subscriptions(self, day: int):
        schema = UserSchema(many=True)
        time_now = datetime.datetime.utcnow()
        date_expired = time_now + datetime.timedelta(days=day)
        query = session.query(User.uuid).join(UsersRoles).filter(
            UsersRoles.date_expiration.between(time_now, date_expired)).all()
        return schema.dump(query)
        # TODO ниже запрос, если нужен еще и id роли
        # session.query(User.uuid.label("user"), Role.uuid.label("role")).join(UsersRoles,
        #                                                                      UsersRoles.users_uuid == User.uuid).join(
        #     Role, Role.uuid == UsersRoles.roles_uuid).filter(
        #     UsersRoles.date_expiration.between(time_now, date_expired)).all()
