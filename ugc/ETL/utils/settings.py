import logging
from logging import config as log_conf

from pydantic import BaseSettings, Field

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': log_format,
        },
    },
    'handlers': {
        'console': {
            'formatter': 'console',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': [
            'console',
        ],
    }
}

logging.basicConfig(filename="ugc.log", level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger('log')
log_conf.dictConfig(LOGGING)


class Settings(BaseSettings):
    kafka_host: str = Field("localhost", env="KAFKA_HOST")
    kafka_port: str = Field("9092", env="KAFKA_PORT")
    topic: str = Field("views", env="KAFKA_TOPIC")

    clickhouse_host: str = Field("localhost", env="CLICKHOUSE_HOST")
    batch_size: int = 1


