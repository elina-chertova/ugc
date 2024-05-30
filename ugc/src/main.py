"""Script to run FastAPI UGC service."""
import sentry_sdk
import uvicorn
from aiokafka import AIOKafkaProducer
from api.v1 import bookmarks, rating, review, views
from asynch import connect
from core.config import Settings
from core.logger import LOGGING
from db import clickhouse, kafka, mongodb
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(integrations=[FastApiIntegration()])

conf = Settings()

PROJECT_NAME = 'UGC Service'

app = FastAPI(
    title=PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    description='UGC service with comment, views and other people actions.',
    version='1.0.0',
)
app.add_middleware(SentryAsgiMiddleware)


@app.on_event('startup')
async def startup():
    """Start databases."""
    kafka.producer = AIOKafkaProducer(bootstrap_servers='{0}:{1}'.format(conf.kafka_host, conf.kafka_port))
    clickhouse.clickhouse = await connect(host=conf.clickhouse_host, port=int(conf.clickhouse_port))
    mongodb.mongodb = AsyncIOMotorClient(host=conf.mongodb_host, port=int(conf.mongodb_port), directConnection=True)
    await kafka.producer.start()


@app.on_event('shutdown')
async def shutdown():
    await kafka.producer.stop()
    mongodb.mongodb.close()

app.include_router(views.router, prefix='/api/v1/views', tags=['Views'])
app.include_router(rating.router, prefix='/api/v1/rating', tags=['Rating'])
app.include_router(bookmarks.router, prefix='/api/v1/bookmarks', tags=['Bookmarks'])
app.include_router(review.router, prefix='/api/v1/review', tags=['Review'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=conf.app_port,
        log_config=LOGGING
    )
