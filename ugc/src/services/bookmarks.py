import logging
from functools import lru_cache

from api.utils import messages
from db.mongodb import get_mongodb
from fastapi import Depends
from models.user import BookmarkModel
from motor.motor_asyncio import AsyncIOMotorClient
from services.utils import BaseUser
from storage.mongodb import MongoDB

logger = logging.getLogger(__name__)


class Bookmarks(BaseUser):
    def __init__(self, storage):
        self.storage = storage

    @property
    def database(self) -> str:
        return 'Bookmarks'

    async def send(self, user_id: str, movie_id: str) -> str:
        """
        Set bookmark if it doesn't exist, else delete bookmark.
        :param user_id:
        :param movie_id:
        :return:
        """
        document = {'user_id': user_id, 'movie_id': movie_id}
        params = {'$and': [{'user_id': user_id}, {'movie_id': movie_id}]}
        is_exists = await self.storage.get_one(database=self.database, params=params)
        if is_exists is None:
            await self.storage.send(database=self.database, document=document)
            logger.info('Bookmark for the movie {0} is added by user {1}'.format(movie_id, user_id))
            return messages.add_bookmark
        await self.storage.delete_one(database=self.database, params=params)
        logger.info('Bookmark for the movie {0} is deleted by user {1}'.format(movie_id, user_id))
        return messages.del_bookmark

    async def delete(self, user_id: str, movie_id: str) -> str:
        """
        Delete user's bookmark.
        :param user_id:
        :param movie_id:
        :return:
        """
        params = {'$and': [{'user_id': user_id}, {'movie_id': movie_id}]}
        is_exists = await self.storage.get_one(database=self.database, params=params)
        if is_exists is not None:
            await self.storage.delete_one(database=self.database, params=params)
            logger.info('Bookmark for the movie {0} is deleted by user {1}'.format(movie_id, user_id))
            return messages.del_bookmark
        return messages.bookmark_n_ex

    async def get(self, user_id):
        """
        Get all user's bookmarks.
        :param user_id:
        :return:
        """
        params = {'user_id': user_id}
        filter_ = {"_id": 0, 'user_id': 0}
        all_bookmarks = await self.storage.get(database=self.database, params=params, filter_=filter_)
        result = [BookmarkModel(movie_id=item['movie_id']) for item in all_bookmarks]
        logger.info('Users bookmarks {0}'.format(user_id))
        return result


@lru_cache()
def get_bookmarks_service(
    storage: AsyncIOMotorClient = Depends(get_mongodb),
) -> Bookmarks:
    storage = MongoDB(storage)
    return Bookmarks(storage)
