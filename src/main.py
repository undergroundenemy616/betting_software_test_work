import logging

import sentry_sdk
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from api import base
from core.config import settings
from core.logger import LOGGING
from db import mongo_adapter

app = FastAPI(
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    title="BETTING_SOFTWARE_TEST_WORK",
    description="Тестовое задание",
    version="1.0.0",
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    mongo_adapter.mongo_client = AsyncIOMotorClient(settings.MONGO_DETAILS)


@app.on_event('shutdown')
async def shutdown():
    await mongo_adapter.mongo_client.close()

sentry_sdk.init(dsn=settings.SENTRY_DSN)


app.logger = logging.getLogger(__name__)
app.logger.setLevel(logging.INFO)


app.include_router(base.router, prefix='/api')

app.add_middleware(SentryAsgiMiddleware)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG
    )
