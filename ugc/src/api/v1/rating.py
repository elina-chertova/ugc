import logging
from http import HTTPStatus

from check_data.check_auth import get_user
from check_data.check_movie import check_movie
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from models.views import Success
from services.rating import Rating, get_rating_service

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post('/{movie_id}/rating/send',
             summary="Send movie's rating.")
async def set_rating(request: Request, movie_id: str = Query(None, description="Movie ID"),
                     score: int = Query(None, description="Movie score"),
                     storage: Rating = Depends(get_rating_service)):
    user, user_code = await get_user(request)
    msg, movie_code = await check_movie(movie_id)

    if user_code == HTTPStatus.OK and movie_code == HTTPStatus.OK:
        res = await storage.send(user, movie_id, score)
        return Success(message=res, code=HTTPStatus.OK)
    elif movie_code != HTTPStatus.OK:
        raise HTTPException(status_code=movie_code, detail=msg['detail'])
    raise HTTPException(status_code=user_code, detail=user)


@router.get('/{movie_id}/rating/get',
            summary="Get average rating")
async def get_rating(movie_id: str = Query(None, description="Movie ID"),
                     storage: Rating = Depends(get_rating_service)):
    msg, movie_code = await check_movie(movie_id)
    if movie_code == HTTPStatus.OK:
        result = await storage.get(movie_id)
        return result
    raise HTTPException(status_code=movie_code, detail=msg['detail'])

