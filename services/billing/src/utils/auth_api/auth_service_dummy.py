from typing import Optional

from utils.auth_api.base import AbstractAuth, UserSchema


class DummyAuthAPI(AbstractAuth):
    def __init__(self, users: dict[str, UserSchema]):
        self.users = users

    def get_user_info(self, user_uuid: str) -> Optional[UserSchema]:
        user_info = self.users.get(user_uuid)
        if not user_info:
            return None
        return user_info
