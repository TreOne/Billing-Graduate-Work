from datetime import datetime, timedelta
from http.client import BAD_REQUEST, CONFLICT, NOT_FOUND
from typing import Optional

import pyotp
from sqlalchemy import or_

from auth_api.api.v1.schemas.user import UserSchema
from auth_api.api.v1.schemas.view import ExpiringSubscriptionSchema
from auth_api.commons.jwt_utils import deactivate_all_refresh_tokens
from auth_api.commons.pagination import paginate
from auth_api.database import session
from auth_api.extensions import db
from auth_api.models.user import AuthHistory, Role, User, UsersRoles
from auth_api.services.exceptions import ServiceException


class UserServiceException(ServiceException):
    pass


class UserService:
    def get_auth_history(self, user_uuid: str):
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
        schema = ExpiringSubscriptionSchema(many=True)
        time_now = datetime.utcnow()
        date_expired = time_now + timedelta(days=day)
        query = session.query(
            User.uuid.label("user_uuid"),
            Role.uuid.label("role_uuid")
        ).join(
            UsersRoles,
            UsersRoles.users_uuid == User.uuid
        ).join(
            Role,
            Role.uuid == UsersRoles.roles_uuid
        ).filter(
            UsersRoles.date_expiration.between(time_now, date_expired)
        ).all()
        return schema.dump(query)

    def get_user_roles(self, user_uuid: str):
        user = session.query(User).get(user_uuid)
        if not user:
            raise UserServiceException('User not found.', http_code=NOT_FOUND)
        return user.roles

    def user_has_role(self, user_uuid: str, role_uuid: str):
        user = session.query(UsersRoles).filter_by(users_uuid=user_uuid, roles_uuid=role_uuid).first()
        return bool(user)

    def add_role_to_user(self, user_uuid: str, role_uuid: str, expiration_months: Optional[int] = None):
        user = session.query(User).get(user_uuid)
        if not user:
            raise UserServiceException('User not found.', http_code=NOT_FOUND)
        role = session.query(Role).get(role_uuid)
        if not role:
            raise UserServiceException('Role not found.', http_code=NOT_FOUND)
        date_expiration = None
        if expiration_months:
            date_expiration = datetime.utcnow() + timedelta(
                days=expiration_months * 31)  # TODO: Придумать способ лучше
        add_role = UsersRoles(
            users_uuid=user_uuid,
            roles_uuid=role_uuid,
            date_expiration=date_expiration,
        )
        session.add(add_role)
        session.commit()

        return user.roles

    def update_role_exp_date(self, user_uuid: str, role_uuid: str, expiration_months=1):
        user_role = session.query(UsersRoles).filter_by(users_uuid=user_uuid, roles_uuid=role_uuid).first()
        old_date_expiration = user_role.date_expiration
        if old_date_expiration < datetime.utcnow():
            old_date_expiration = datetime.utcnow()
        date_expiration = None
        if expiration_months:
            date_expiration = old_date_expiration + timedelta(days=expiration_months * 31)
        user_role.date_expiration = date_expiration

        session.commit()
        user_roles = session.query(User).get(user_uuid).roles
        return user_roles

    def delete_user_role(self, user_uuid: str, role_uuid: str):
        user = session.query(User).get(user_uuid)
        if not user:
            raise UserServiceException('User not found.', http_code=NOT_FOUND)
        role = session.query(Role).get(role_uuid)
        if not role:
            raise UserServiceException('Role not found.', http_code=NOT_FOUND)

        if role in user.roles:
            user.roles.remove(role)
        else:
            raise UserServiceException('The user does not have this role.', http_code=CONFLICT)

        session.add(user)
        session.commit()

        return user.roles
