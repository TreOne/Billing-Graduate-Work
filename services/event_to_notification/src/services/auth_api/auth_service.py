from http import HTTPStatus
from typing import Optional

import requests
import logging

from services.auth_api.base import AbstractAuth, UserSchema

logger = logging.getLogger(__name__)


class AuthAPI(AbstractAuth):
    def __init__(self, api_url: str, username: str, password: str):
        self.api_url = api_url
        self.__username = username
        self.__password = password
        self.__refresh_token = ''
        self.__access_token = ''
        self.__get_user_url = 'api/v1/users/'
        self.__refresh_token_url = 'auth/v1/refresh'
        self.__login_url = 'auth/v1/login'

    def get_user_info(self, user_uuid: str) -> Optional[UserSchema]:
        response = self._get(f'{self.__get_user_url}{user_uuid}')
        if response.status_code != HTTPStatus.OK:
            logger.error(f"Can't retrieve {user_uuid},response status{response.status_code}")
            return None
        user_data = response.json().get('user')
        return UserSchema(**user_data)

    def _abs_url(self, path: str) -> str:
        return f'{self.api_url}{path}'

    def _get(self, path: str, headers=None) -> requests.request:
        url = self._abs_url(f'{path}')
        headers = headers or self._get_headers()
        response = requests.get(url, headers)

        if response.status_code == 200:
            return response

        if 400 <= response.status_code <= 499:
            is_refresh_success = self._refresh_tokens()
            if not is_refresh_success:
                self._login()

        response = requests.get(url, headers=self._get_headers())
        return response

    def _refresh_tokens(self):
        header = {
            'Content-type': 'application/json',
            'Authorization': f'Bearer {self.__refresh_token}',
        }
        url = self._abs_url(self.__refresh_token_url)
        response = requests.post(url, headers=header)
        if response.status_code == 200:
            tokens = response.json()
            self.__refresh_token = tokens['refresh_token']
            self.__access_token = tokens['access_token']
            return True
        return False

    def _login(self):
        url = self._abs_url(self.__login_url)
        data = {
            'username': self.__username,
            'password': self.__password,
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            tokens = response.json()
            self.__refresh_token = tokens['refresh_token']
            self.__access_token = tokens['access_token']
            return True
        else:
            logger.error(f'Uth service login error , status{response.status_code}')
        return False

    def _get_headers(self):
        header = {
            'Content-type': 'application/json',
            'Authorization': f'Bearer {self.__access_token}',
        }
        return header
