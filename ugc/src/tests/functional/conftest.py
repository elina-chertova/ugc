
import asyncio

import aiohttp
import pytest

from .settings import TestSettings

settings = TestSettings()


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture(scope='session')
def make_request(session):
    async def inner(service_url: str, req_type: str, path: str, json: dict = None, headers: dict = None):
        requests: dict = {"post": session.post, "get": session.get, "delete": session.delete}
        json = json or {}
        headers = headers or None
        async with requests[req_type](service_url + path, json=json, headers=headers) as response:
            body = await response.json()
            status = response.status
            return body, status
    return inner
