from functools import lru_cache

from core.settings import get_settings
from services.auth_service import AuthAPI
from services.kafka_consumer import ConsumerKafka

settings = get_settings()


class Consumer(ConsumerKafka):
    configs = settings.kafka


class AuthDataEnricher(AuthAPI):
    api_url = settings.auth_api_url


@lru_cache
def get_user_data_service():
    user_data_service = AuthDataEnricher()
    user_data_service.login(username=settings.auth_login, password=settings.auth_password)
    return user_data_service
