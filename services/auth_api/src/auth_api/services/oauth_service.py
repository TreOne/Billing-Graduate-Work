import uuid
from http.client import FORBIDDEN, NOT_FOUND

from auth_api.commons.oauth.clients import OAuthClient
from auth_api.commons.utils import generate_password
from auth_api.database import session
from auth_api.models.user import User
from auth_api.services.exceptions import ServiceException


class OAuthServiceException(ServiceException):
    pass


class OAuthService:
    def login_user_oauth(self, social_id: str, email: str):
        user = session.query(User).filter_by(social_id=social_id).first()
        if user is None:
            email_exist = session.query(User).filter_by(email=email).first()
            if email_exist:
                email = None

            user = User(
                username=f'Unknown-{uuid.uuid4()}',
                email=email,
                password=generate_password(),
                social_id=social_id,
            )
            session.add(user)
            session.commit()

        if not user.is_active:
            raise OAuthServiceException('Your account is blocked.', http_code=FORBIDDEN)
        return user.uuid

    def get_user_info_from_oauth(self, provider: str):
        provider_oauth = OAuthClient.get_provider(provider)
        if not provider_oauth:
            raise OAuthServiceException('OAuth provider not found.', http_code=NOT_FOUND)

        user_info = provider_oauth.get_user_info()
        if not user_info:
            raise OAuthServiceException('Authentication failed.', http_code=FORBIDDEN)

        social_id = user_info['social_id']
        email = user_info['email']
        return social_id, email

    def get_providers_list_oauth(self):
        if OAuthClient.providers is None:
            OAuthClient.load_providers()
        providers = list(OAuthClient.providers.keys())
        providers_data = []
        for provider in providers:
            providers_data.append(
                {
                    'name': provider,
                    'properties': OAuthClient.get_provider(provider).get_data_for_authorize(),
                },
            )
        return providers_data
