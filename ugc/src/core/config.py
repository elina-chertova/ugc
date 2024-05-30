import os

from pydantic import BaseSettings, Field

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


PROJECT_NAME = os.getenv('FasterAPI', 'UGC Service')
localhost = '127.0.0.1'


class Settings(BaseSettings):
    movie_service_host = Field(localhost, env='MOVIE_SERVICE_HOST')
    movie_service_port = Field('8005', env="MOVIE_SERVICE_PORT")

    auth_service_host = Field(localhost, env='AUTH_SERVICE_HOST')
    auth_service_port = Field('5000', env="AUTH_SERVICE_PORT")

    kafka_host: str = Field('localhost', env="KAFKA_HOST")
    kafka_port: str = Field('9092', env="KAFKA_PORT")
    # clickhouse-node-1
    clickhouse_host: str = Field('localhost', env="CLICKHOUSE_HOST")
    clickhouse_port: str = Field('9000', env="CLICKHOUSE_PORT")

    service_host: str = Field('localhost', env='SERVICE_HOST')

    mongodb_host: str = Field('localhost', env='MONGODB_HOST')
    mongodb_port: str = Field('27017', env='MONGODB_PORT')
    app_port: int = 8003
