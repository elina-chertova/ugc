from http import HTTPStatus

import pytest

from ..data.user_data import (add_score, movie_rating_1, movie_rating_2,
                              score_ex, user_rating_1, user_rating_2)
from ..settings import TestSettings
from ..utils.get_valid_user import request_users

settings = TestSettings()


@pytest.mark.parametrize(
    'user_info, movie_id, expected_answer',
    [
        (
                user_rating_1,
                movie_rating_1,
                {'status': HTTPStatus.OK, 'body': add_score}
        ),
        (
                user_rating_1,
                movie_rating_1,
                {'status': HTTPStatus.OK, 'body': score_ex}
        ),
    ]
)
@pytest.mark.asyncio
async def test_add_rating(make_request, user_info, movie_id, expected_answer):
    body, status, access_headers, refresh_headers = await request_users(make_request, user_info)

    url = 'rating/{0}/rating/send?score=5'.format(movie_id)
    body, status = await make_request(settings.UGC_URL, 'get', url, headers=access_headers)

    assert body == expected_answer['body']
    assert status == expected_answer['status']


@pytest.mark.parametrize(
    'user_info, movie_id, expected_answer',
    [
        (
                user_rating_2,
                movie_rating_2,
                {'status': HTTPStatus.OK, 'body': 6.0}
        ),
    ]
)
@pytest.mark.asyncio
async def test_avg_rating(make_request, user_info, movie_id, expected_answer):

    for i, user_id in enumerate(user_info):
        body, status, access_headers, refresh_headers = await request_users(make_request, user_id)

        url = 'rating/{0}/rating/send?score={1}'.format(movie_id, i + 5)
        _, _ = await make_request(settings.UGC_URL, 'get', url, headers=access_headers)

    url = 'rating/{0}/rating/get'.format(movie_id)
    body, status = await make_request(settings.UGC_URL, 'get', url)

    assert body == expected_answer['body']
    assert status == expected_answer['status']

