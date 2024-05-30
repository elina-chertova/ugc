import logging
from http import HTTPStatus

from api.utils.messages import data_in_kafka
from api.utils.paginator import Paginator
from check_data.check_auth import get_user
from check_data.check_movie import check_movie
from fastapi import APIRouter, Depends, HTTPException, Request
from models.views import Error, View
from services.views_history import Views, get_views_service

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get('/history/views',
            summary="Get views history from Clickhouse.",
            response_description="Views history.",
            description="Get view history from Clickhouse using user ID.",
            tags=['Views'])
async def get_history(request: Request, storage: Views = Depends(get_views_service), paginator: Paginator = Depends()):
    user, user_code = await get_user(request)
    if user_code == HTTPStatus.OK:
        views = await storage.get_history(user_id=user, page=paginator.page_number, page_size=paginator.page_size)
        return views
    return Error(message=user, code=int(user_code))


@router.post('/{film_id}/view',
             summary="Send view info to Kafka.",
             response_description="Code 200 if data was sent to Kafka, else something went wrong.",
             description="Send view info in seconds to Kafka.",
             tags=['Views'])
async def movie_pause(request: Request, film_id: str, user_time: int, movie_time: int,
                      event_source: Views = Depends(get_views_service)):
    user, user_code = await get_user(request)
    msg, movie_code = await check_movie(film_id)

    if user_code == HTTPStatus.OK and movie_code == HTTPStatus.OK:
        await event_source.send_view_info(user_time, user, film_id, movie_time)
        return data_in_kafka
    elif movie_code != HTTPStatus.OK:
        raise HTTPException(status_code=movie_code, detail=msg['detail'])
    raise HTTPException(status_code=user_code, detail=user)
