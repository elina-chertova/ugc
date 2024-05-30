from http import HTTPStatus

import pytest

from ..data.movie_data import wrong_movie, wrong_movie_msg
from ..data.user_data import (book_add, book_del, movie_book_add, movie_ids,
                              movie_ids_res, user_bookmark_1, user_bookmark_2)
from ..settings import TestSettings
from ..utils.get_valid_user import request_users

settings = TestSettings()


async def bookmark(make_request, movie_ids_uuid: list, access_headers: str):
    for movie_id in movie_ids_uuid:
        url = 'bookmarks/{0}/bookmarks/add'.format(movie_id)
        _, _ = await make_request(settings.UGC_URL, 'get', url, headers=access_headers)


@pytest.mark.parametrize(
    'user_info, movie_id, expected_answer',
    [
        (
                user_bookmark_1,
                movie_book_add,
                {'status': HTTPStatus.OK, 'body': book_add}
        ),
        (
                user_bookmark_1,
                wrong_movie,
                {'status': HTTPStatus.NOT_FOUND, 'body': wrong_movie_msg}
        ),
        (
                user_bookmark_1,
                movie_book_add,
                {'status': HTTPStatus.OK, 'body': book_del}
        ),
    ]
)
@pytest.mark.asyncio
async def test_add_bookmark(make_request, user_info, movie_id, expected_answer):
    body, status, access_headers, refresh_headers = await request_users(make_request, user_info)

    url = 'bookmarks/{0}/bookmarks/add'.format(movie_id)
    body, status = await make_request(settings.UGC_URL, 'get', url, headers=access_headers)

    assert body == expected_answer['body']
    assert status == expected_answer['status']


@pytest.mark.parametrize(
    'user_info, movie_ids, expected_answer',
    [
        (
                user_bookmark_2,
                movie_ids,
                {'status': HTTPStatus.OK, 'body': movie_ids_res}
        ),
    ]
)
@pytest.mark.asyncio
async def test_all_bookmark(make_request, user_info, movie_ids, expected_answer):
    body, status, access_headers, refresh_headers = await request_users(make_request, user_info)

    # add bookmarks
    await bookmark(make_request, movie_ids, access_headers)

    url = 'bookmarks/bookmarks/all'
    body, status = await make_request(settings.UGC_URL, 'get', url, headers=access_headers)

    assert body == expected_answer['body']
    assert status == expected_answer['status']

    # clear bookmarks
    await bookmark(make_request, movie_ids, access_headers)







