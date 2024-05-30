from http import HTTPStatus

import pytest

from ..data.user_data import (comment_add, comment_ex, movie_rating_1,
                              movie_rating_2, movie_rating_3, user_review_1)
from ..settings import TestSettings
from ..utils.get_valid_user import request_users

settings = TestSettings()


@pytest.mark.parametrize(
    'user_info, movie_id, expected_answer',
    [
        (
                user_review_1,
                movie_rating_1,
                {'status': HTTPStatus.OK, 'body': comment_add}
        ),
        (
                user_review_1,
                movie_rating_1,
                {'status': HTTPStatus.OK, 'body': comment_ex}
        ),
    ]
)
@pytest.mark.asyncio
async def test_add_review(make_request, user_info, movie_id, expected_answer):
    body, status, access_headers, refresh_headers = await request_users(make_request, user_info)

    url = 'review/{0}/review/add?text=Hello, World.'.format(movie_id)
    body, status = await make_request(settings.UGC_URL, 'get', url, headers=access_headers)

    assert body == expected_answer['body']
    assert status == expected_answer['status']


@pytest.mark.parametrize(
    'user_info, movie_id, expected_answer',
    [
        (
                user_review_1,
                movie_rating_2,
                {'status': HTTPStatus.OK, 'body': 1}
        ),
    ]
)
@pytest.mark.asyncio
async def test_all_review(make_request, user_info, movie_id, expected_answer):
    body, status, access_headers, refresh_headers = await request_users(make_request, user_info)

    url = 'review/{0}/review/add?text=Hello, World.'.format(movie_id)

    _, _ = await make_request(settings.UGC_URL, 'get', url, headers=access_headers)

    url = 'review/{0}/review/all'.format(movie_id)
    body, status = await make_request(settings.UGC_URL, 'get', url, headers=access_headers)
    assert len(body) == expected_answer['body']
    assert status == expected_answer['status']


@pytest.mark.parametrize(
    'user_info, movie_id, expected_answer',
    [
        (
                user_review_1,
                movie_rating_3,
                {'status': HTTPStatus.OK, 'body': 0}
        ),
    ]
)
@pytest.mark.asyncio
async def test_wrong_all_review(make_request, user_info, movie_id, expected_answer):
    body, status, access_headers, refresh_headers = await request_users(make_request, user_info)
    url = 'review/{0}/review/all'.format(movie_id)
    body, status = await make_request(settings.UGC_URL, 'get', url, headers=access_headers)
    assert len(body) == expected_answer['body']
    assert status == expected_answer['status']
