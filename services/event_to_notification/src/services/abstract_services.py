from abc import abstractmethod, ABC


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
