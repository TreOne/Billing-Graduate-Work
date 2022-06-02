import asyncio
from dataclasses import dataclass

import aiohttp
import pytest
from config.settings import NOTIFICATION_SERVICE_URL
from multidict._multidict import CIMultiDictProxy


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
async def access_token() -> dict:
    token: str = 'JWT'
    return {'Authorization': f'Bearer {token}'}


@pytest.fixture
def make_request(session):
    dispatcher: dict = {
        'get': session.get,
        'post': session.post,
        'patch': session.patch,
        'put': session.put,
        'delete': session.delete,
    }

    async def inner(
        http_method: str,
        data=None,
        headers: str = None,
        endpoint: str = None,
    ) -> HTTPResponse:
        """
        :param headers: str
            Дополнительные headers внутри запроса
        :param http_method: str
            HTTP метод который будет использован
        :param endpoint: str
            Путь до нашего конечного url
        :param data: Optional[dict]
            Тело запроса
        :return: HTTPResponse
        """
        if data is None:
            data = {}
        async with dispatcher.get(http_method)(
            url=f'{NOTIFICATION_SERVICE_URL}{endpoint}',
            headers=headers,
            json=data,
        ) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner
