import http
from http import HTTPStatus
from typing import TypedDict

import requests
from django.conf import settings

from utils.auth_api.base import AbstractAuth
from utils.schemas.user_subscribe import UserSubscribeSchema


class LoginData(TypedDict):
    username: str
    password: str


class AuthAPI(AbstractAuth):
    def __init__(self, username: str, password: str):
        self.api_url = settings.AUTH_SERVICE_URL
        self.__username = username
        self.__password = password
        self.__refresh_token = ''
        self.__access_token = ''
        self.__get_subscriptions_end = settings.AUTH_SERVICE_URL_SUBSCRIPTIONS_END
        self.__refresh_token_url = settings.AUTH_SERVICE_URL_REFRESH
        self.__login_url = settings.AUTH_SERVICE_URL_LOGIN

    def get_user_subscriptions_end(self, days: int) -> list[UserSubscribeSchema]:
        response = self._get(f'{self.__get_subscriptions_end}?days={days}')
        if response.status_code != HTTPStatus.OK:
            return []
        subscriptions_end: list[UserSubscribeSchema] = [
            UserSubscribeSchema(**user_sub) for user_sub in response.json().get('results')
        ]
        return subscriptions_end

    def _abs_url(self, path: str) -> str:
        return f'{self.api_url}{path}'

    def _get(self, path: str, headers=None) -> requests.Response:
        url = self._abs_url(f'{path}')
        headers = headers or self._get_headers()
        response = requests.get(url, headers)

        if response.status_code == http.HTTPStatus.OK:
            return response

        if 400 <= response.status_code <= 499:
            is_refresh_success = self._refresh_tokens()
            if not is_refresh_success:
                self._login()

        response = requests.get(url, headers=self._get_headers())
        return response

    def _refresh_tokens(self) -> bool:
        header = {
            'Content-type': 'application/json',
            'Authorization': f'Bearer {self.__refresh_token}',
        }
        url = self._abs_url(self.__refresh_token_url)
        response = requests.post(url, headers=header)
        if response.status_code == http.HTTPStatus.OK:
            tokens = response.json()
            self.__refresh_token = tokens['refresh_token']
            self.__access_token = tokens['access_token']
            return True
        return False

    def _login(self) -> bool:
        url = self._abs_url(self.__login_url)
        data: LoginData = LoginData(
            username=self.__username, password=self.__password,
        )
        response = requests.post(url, json=data)
        if response.status_code == http.HTTPStatus.OK:
            tokens = response.json()
            self.__refresh_token = tokens['refresh_token']
            self.__access_token = tokens['access_token']
            return True
        return False

    def _get_headers(self) -> dict[str, str]:
        header = {
            'Content-type': 'application/json',
            'Authorization': f'Bearer {self.__access_token}',
        }
        return header
