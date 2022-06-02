from abc import abstractmethod, ABC
from functools import lru_cache

from services.auth_service import AUTH_API_URL, AuthAPI


class AbstractConsumer(ABC):
    @abstractmethod
    def consume(self):
        raise NotImplementedError


class AbstractAuth(ABC):
    @abstractmethod
    def login(self, username: str, password: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_user_info(self, user_uuid: str):
        raise NotImplementedError


@lru_cache
def get_auth_api():
    return AuthAPI(AUTH_API_URL)

