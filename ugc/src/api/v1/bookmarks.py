import logging
from http import HTTPStatus

from check_data.check_auth import get_user
from check_data.check_movie import check_movie
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from models.views import Success
from services.bookmarks import Bookmarks, get_bookmarks_service

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post('/{movie_id}/bookmarks/add',
             summary="Add or delete user's bookmark for the movie.")
async def set_bookmarks(request: Request, movie_id: str = Query(None, description="Movie ID"),
                        storage: Bookmarks = Depends(get_bookmarks_service)):
    user, user_code = await get_user(request)
    msg, movie_code = await check_movie(movie_id)

    if user_code == HTTPStatus.OK and movie_code == HTTPStatus.OK:
        status = await storage.send(user, movie_id)
        return Success(message=status, code=HTTPStatus.OK)
    elif movie_code != HTTPStatus.OK:
        raise HTTPException(status_code=movie_code, detail=msg['detail'])
    raise HTTPException(status_code=user_code, detail=user)


@router.get('/bookmarks/all',
            summary="Show all user's bookmarks.")
async def get_bookmarks(request: Request, storage: Bookmarks = Depends(get_bookmarks_service)):
    user, user_code = await get_user(request)

    if user_code == HTTPStatus.OK:
        bookmarks = await storage.get(user)
        return bookmarks
    raise HTTPException(status_code=user_code, detail=user)

