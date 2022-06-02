import http

import pytest
from notification.schemas import EmailBody

pytestmark = pytest.mark.asyncio


async def test_unauthorized_get_profile(make_request, access_token):

    demo_data = {
        'recipient': 'user@example.com',
        'subject': 'Hello, world!',
        'body': '<p>Lorem ipsum</p>',
        'immediately': False,
        'log_it': False,
        'ttl': 86400,
    }

    body: EmailBody = EmailBody(
        **demo_data,
    )

    response = await make_request(
        endpoint='/api/v1/send/email/',
        http_method='post',
        headers=access_token,
        data=body.json(),
    )
    assert response.status == http.HTTPStatus.OK
