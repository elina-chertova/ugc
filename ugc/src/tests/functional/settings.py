from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    AUTH_HOST: str = Field('127.0.0.1', env='AUTH_HOST')
    AUTH_PORT: str = Field('5000', env='AUTH_PORT')
    AUTH_URL: str = Field('http://0.0.0.0:5000/', env='AUTH_URL')

    UGC_HOST: str = Field('127.0.0.1', env='UGC_HOST')
    UGC_PORT: str = Field('8003', env='UGC_PORT')
    UGC_URL: str = Field('http://0.0.0.0:8003/api/v1/', env='UGC_URL')


