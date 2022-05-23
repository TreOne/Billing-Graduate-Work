import logging

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

import api
from connectors.rabbitmq import rabbitmq_connect, rabbitmq_disconnect, rabbitmq_prepare
from connectors.redis import redis_connect, redis_disconnect
from core import config

logger = logging.getLogger('app')

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url='/openapi',
    openapi_url='/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    rabbitmq_connect()
    rabbitmq_prepare()
    await redis_connect()


@app.on_event('shutdown')
async def shutdown():
    rabbitmq_disconnect()
    await redis_disconnect()


app.include_router(api.router)
