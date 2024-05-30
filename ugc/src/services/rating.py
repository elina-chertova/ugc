import logging
from functools import lru_cache

from api.utils import messages
from db.mongodb import get_mongodb
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient
from services.utils import BaseUser
from storage.mongodb import MongoDB

logger = logging.getLogger(__name__)


class Rating(BaseUser):
    def __init__(self, storage):
        self.storage = storage

    @property
    def database(self) -> str:
        return 'Rating'

    async def send(self, user_id: str, movie_id: str, score: int) -> str:
        """
        Set user's score of a movie.
        :param user_id:
        :param movie_id:
        :param score:
        :return:
        """
        document = {'user_id': user_id,
                    'movie_id': movie_id,
                    'rating': score}
        params = {'$and': [{'user_id': user_id}, {'movie_id': movie_id}]}
        is_exists = await self.storage.get_one(self.database, params)
        if is_exists is None:
            await self.storage.send(self.database, document)
            logger.info('Score is sent to MongoDB: user_id {0}, movie_id: {1}'.format(user_id, movie_id))
            return messages.send_score
        logger.info('Score already exists: user_id {0}, movie_id: {1}'.format(user_id, movie_id))
        return messages.score_exists

    async def get(self, movie_id):
        """
        Get the average score of a movie.
        :param movie_id:
        :return:
        """
        params = [{'$match': {"movie_id": movie_id}},
                  {'$group': {'_id': 1, 'all': {'$sum': '$rating'}, 'count': {'$sum': 1}}}]
        rating_res = await self.storage.aggregate(self.database, params)
        average_rating = rating_res[0]['all'] / rating_res[0]['count']
        logger.info('Average score of the movie {0} = {1}'.format(movie_id, average_rating))
        return average_rating


@lru_cache()
def get_rating_service(
    storage: AsyncIOMotorClient = Depends(get_mongodb),
) -> Rating:
    storage = MongoDB(storage)
    return Rating(storage)




