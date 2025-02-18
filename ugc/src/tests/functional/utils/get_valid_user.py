from ..settings import TestSettings

settings = TestSettings()


async def request_users(make_request, data):
    _, _ = await make_request(settings.AUTH_URL, 'post', 'registration', json=data)
    body, status = await make_request(settings.AUTH_URL, 'post', 'login', json=data)

    access_headers = {"Authorization": "Bearer {0}".format(body['access_token'])}
    refresh_headers = {"Authorization": "Bearer {0}".format(body['refresh_token'])}
    return body, status, access_headers, refresh_headers
