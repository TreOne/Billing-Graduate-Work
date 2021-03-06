from http.client import BAD_REQUEST, CONFLICT, FORBIDDEN

import pyotp
from sqlalchemy import or_

from auth_api.api.v1.schemas.user import UserSchema
from auth_api.commons.jwt_utils import create_tokens
from auth_api.commons.utils import get_device_type
from auth_api.database import session
from auth_api.extensions import pwd_context
from auth_api.models.user import AuthHistory, User
from auth_api.services.exceptions import ServiceException


class AuthServiceException(ServiceException):
    pass


class AuthService:
    def register_user(self, username: str, email: str, password: str):
        schema = UserSchema()
        existing_user = (
            session.query(User)
            .filter(or_(User.username == username, User.email == email),)
            .first()
        )
        if existing_user:
            raise AuthServiceException(
                'Username or email is already taken!', http_code=CONFLICT
            )
        user = User(username=username, email=email, password=password)

        session.add(user)
        session.commit()

        return schema.dump(user)

    def get_tokens(self, username: str, password: str, totp_code: str = ''):
        if not username or not password:
            raise AuthServiceException('Missing username or password.', http_code=BAD_REQUEST)

        user = session.query(User).filter_by(username=username).first()

        if user is None or not pwd_context.verify(password, user.password):
            raise AuthServiceException('Bad credentials.', http_code=BAD_REQUEST)

        if not user.is_active:
            raise AuthServiceException('Your account is blocked.', http_code=FORBIDDEN)

        if user.is_totp_enabled:
            secret = user.two_factor_secret
            totp = pyotp.TOTP(secret)

            if not totp.verify(totp_code):
                raise AuthServiceException('Wrong totp code.', http_code=BAD_REQUEST)

        access_token, refresh_token = create_tokens(user.uuid)
        return access_token, refresh_token

    def add_to_history(self, user_uuid: str, user_agent: str, ip_address: str):
        session.add(
            AuthHistory(
                user_uuid=user_uuid,
                user_agent=user_agent,
                ip_address=ip_address,
                device=get_device_type(user_agent),
            ),
        )
        session.commit()
