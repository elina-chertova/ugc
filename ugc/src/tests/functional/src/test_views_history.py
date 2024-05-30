from http import HTTPStatus

import pytest

from ..data.movie_data import correct_movie
from ..data.user_data import second_user
from ..settings import TestSettings
from ..utils.get_valid_user import request_users

settings = TestSettings()


@pytest.mark.parametrize(
    'user_info, movie_id, expected_answer',
    [
        (
                second_user,
                correct_movie,
                {'status': HTTPStatus.OK, 'body': 1}
        )
    ]
)
@pytest.mark.asyncio
async def test_views_history(make_request, user_info, movie_id, expected_answer):
    body, status, access_headers, refresh_headers = await request_users(make_request, user_info)

    time = {345: 3452, 124: 543}
    for user_time, movie_time in time.items():
        url = 'views/{0}/view?user_time={1}&movie_time={2}'.format(movie_id, str(user_time), str(movie_time))
        res, _ = await make_request(settings.UGC_URL, 'get', url, headers=access_headers)

    history_url = 'views/history/views?page[size]=1&page[number]=1'
    body, status = await make_request(settings.UGC_URL, 'get', history_url, headers=access_headers)

    assert len(body) == expected_answer['body']
    assert status == expected_answer['status']











# http://0.0.0.0:8003/api/v1/views/history/views?page%5Bsize%5D=5&page%5Bnumber%5D=1




