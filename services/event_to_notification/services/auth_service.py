import requests
from requests import request

from services.base_services import AbstractAuth

AUTH_API_URL = 'http://localhost/auth/'


class AuthAPI(AbstractAuth):
    def __init__(self, api_url):
        self._api_url = api_url
        self.__username = ''
        self.__password = ''
        self.__refresh_token = ''
        self.__access_token = ''

    def login(self, username, password) -> None:
        self.__username = username
        self.__password = password

    def get_user_info(self, user_uuid: str) -> dict[str, any] or int or None:
        response = self._get(f'api/v1/users/{user_uuid}')
        return response.json().get('user') if response.status_code == 200 else None

    def _abs_url(self, path: str) -> str:
        return f'{self._api_url}{path}'

    def _get(self, path: str, headers=None) -> request:
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
        url = self._abs_url('auth/v1/refresh')
        response = requests.post(url, headers=header)
        if response.status_code == 200:
            tokens = response.json()
            self.__refresh_token = tokens['refresh_token']
            self.__access_token = tokens['access_token']
            return True
        return False

    def _login(self):
        url = self._abs_url('auth/v1/login')
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
        return False

    def _get_headers(self):
        header = {
            'Content-type': 'application/json',
            'Authorization': f"Bearer {self.__access_token}",
        }
        return header

