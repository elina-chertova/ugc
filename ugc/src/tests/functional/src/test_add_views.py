from http import HTTPStatus

import pytest

from ..data.movie_data import correct_movie, wrong_movie, wrong_movie_msg
from ..data.user_data import data_in_kafka, user
from ..settings import TestSettings
from ..utils.get_valid_user import request_users

settings = TestSettings()


@pytest.mark.parametrize(
    'user_info, movie_id, expected_answer',
    [
        (
                user,
                correct_movie,
                {'status': HTTPStatus.OK, 'body': data_in_kafka}
        ),
        (
                user,
                wrong_movie,
                {'status': HTTPStatus.NOT_FOUND, 'body': wrong_movie_msg}
        ),
    ]
)
@pytest.mark.asyncio
async def test_add_views(make_request, user_info, movie_id, expected_answer):
    body, status, access_headers, refresh_headers = await request_users(make_request, user_info)

    url = 'views/{0}/view?user_time=345&movie_time=1223'.format(movie_id)
    body, status = await make_request(settings.UGC_URL, 'get', url, headers=access_headers)

    assert body == expected_answer['body']
    assert status == expected_answer['status']










