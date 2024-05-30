import logging
from datetime import datetime
from functools import lru_cache

from api.utils import messages
from db.mongodb import get_mongodb
from fastapi import Depends
from models.user import Comment
from motor.motor_asyncio import AsyncIOMotorClient
from services.utils import BaseUser
from storage.mongodb import MongoDB

logger = logging.getLogger(__name__)


class Review(BaseUser):
    def __init__(self, storage):
        self.storage = storage

    @property
    def database(self) -> str:
        return 'Review'

    async def send(self, user_id: str, movie_id: str, text: str) -> str:
        """
        Send user's review.
        :param user_id:
        :param movie_id:
        :param text:
        :return:
        """
        document = {'user_id': user_id,
                    'movie_id': movie_id,
                    'text': text,
                    'date': datetime.now()}
        params = {'$and': [{'user_id': user_id}, {'movie_id': movie_id}]}
        is_exists = await self.storage.get_one(database=self.database, params=params)
        if is_exists is None:
            await self.storage.send(database=self.database, document=document)
            logger.info('Review is sent to MongoDB {0}, {1}, {2}'.format(user_id, movie_id, text))
            return messages.add_comment
        logger.info('Comment already exists; user: {0}, movie: {1}'.format(user_id, movie_id))
        return messages.comment_exists

    async def delete(self, user_id: str, movie_id: str) -> str:
        """
        Delete user's review.
        :param user_id:
        :param movie_id:
        :return:
        """
        params = {'$and': [{'user_id': user_id}, {'movie_id': movie_id}]}
        is_exists = await self.storage.get_one(database=self.database, params=params)
        if is_exists is not None:
            await self.storage.delete_one(database=self.database, params=params)
            logger.info('Comment has been deleted; user: {0}, movie: {1}'.format(user_id, movie_id))
            return messages.delete_comment
        return messages.comment_n_ex

    async def update(self, user_id: str, movie_id: str, text: str) -> str:
        filter_, update_val = {'$and': [{'user_id': user_id},
                                        {'movie_id': movie_id}]},\
                              {"$set": {
                                  'text': text,
                                  'date': datetime.now()}}

        params = {'$and': [{'user_id': user_id}, {'movie_id': movie_id}]}
        is_exists = await self.storage.get_one(database=self.database, params=params)
        if is_exists is not None:
            await self.storage.update_one(database=self.database, filter_=filter_, update_val=update_val)
            logger.info('Review has been updated by user {0}, movie {1}, new text: {2}'.format(user_id, movie_id, text))
            return messages.update_comment
        return messages.comment_n_ex

    async def get(self, movie_id: str):
        """
        Get all comments of some movie.
        :param movie_id:
        :return:
        """
        params = {'movie_id': movie_id}
        filter_ = {"_id": 0}
        comments = await self.storage.get(database=self.database, params=params, filter_=filter_)
        result = [Comment(user_id=item['user_id'], movie_id=item['movie_id'],
                          text=item['text'], date=item['date']) for item in comments]
        logger.info('Comments for the movie: {0}'.format(movie_id))
        return result


@lru_cache()
def get_review_service(
    storage: AsyncIOMotorClient = Depends(get_mongodb),
) -> Review:
    storage = MongoDB(storage)
    return Review(storage)
