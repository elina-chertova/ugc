import logging
from http import HTTPStatus

from check_data.check_auth import get_user
from check_data.check_movie import check_movie
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from models.views import Success
from services.review import Review, get_review_service

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post('/{movie_id}/review/add',
             summary="Add review.")
async def add_review(request: Request, movie_id: str = Query(None, description="Movie ID"),
                     text: str = Query(None, description="Comment"),
                     storage: Review = Depends(get_review_service)):
    user, user_code = await get_user(request)
    msg, movie_code = await check_movie(movie_id)

    if user_code == HTTPStatus.OK and movie_code == HTTPStatus.OK:
        status = await storage.send(user, movie_id, text)
        return Success(message=status, code=HTTPStatus.OK)
    elif movie_code != HTTPStatus.OK:
        raise HTTPException(status_code=movie_code, detail=msg['detail'])
    raise HTTPException(status_code=user_code, detail=user)


@router.get('/{movie_id}/review/all',
            summary="Show all reviews for movie.")
async def get_reviews(movie_id: str = Query(None, description="Movie ID"),
                     storage: Review = Depends(get_review_service)):
    msg, movie_code = await check_movie(movie_id)
    if movie_code == HTTPStatus.OK:
        comments = await storage.get(movie_id)
        return comments
    raise HTTPException(status_code=movie_code, detail=msg['detail'])


@router.delete('/{movie_id}/review/delete',
               summary="Delete review.")
async def delete_review(request: Request, movie_id: str = Query(None, description="Movie ID"),
                     storage: Review = Depends(get_review_service)):
    user, user_code = await get_user(request)
    msg, movie_code = await check_movie(movie_id)
    if user_code == HTTPStatus.OK and movie_code == HTTPStatus.OK:
        status = await storage.delete(user, movie_id)
        return Success(message=status, code=HTTPStatus.OK)
    elif movie_code != HTTPStatus.OK:
        raise HTTPException(status_code=movie_code, detail=msg['detail'])
    raise HTTPException(status_code=user_code, detail=user)


@router.post('/{movie_id}/review/update',
             summary="Update review.")
async def update_review(request: Request, movie_id: str = Query(None, description="Movie ID"),
                     text: str = Query(None, description="Comment"),
                     storage: Review = Depends(get_review_service)):
    user, user_code = await get_user(request)
    msg, movie_code = await check_movie(movie_id)
    if user_code == HTTPStatus.OK and movie_code == HTTPStatus.OK:
        status = await storage.update(user, movie_id, text)
        return Success(message=status, code=HTTPStatus.OK)
    elif movie_code != HTTPStatus.OK:
        raise HTTPException(status_code=movie_code, detail=msg['detail'])
    raise HTTPException(status_code=user_code, detail=user)
