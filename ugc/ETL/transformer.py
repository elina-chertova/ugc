from dataclasses import dataclass
from datetime import datetime

from utils.settings import logger


@dataclass
class KafkaView:
    key: str
    value: str
    timestamp: int

    def date(self) -> datetime:
        return datetime.utcfromtimestamp(self.timestamp / 1000)

    def movie_user(self) -> (str, str):
        ids = self.key.split('+')
        try:
            movie_id: str = ids[0]
            user_id: str = ids[1]
        except ValueError as e:
            logger.info('Error: {0}'.format(e))
            return None, None
        return user_id, movie_id

    def view(self) -> (str, str):
        times = self.value.split('+')
        try:
            views_time: int = int(times[0])
            movie_time: int = int(times[1])
        except ValueError as e:
            logger.info('Error: {0}'.format(e))
            return None, None
        return views_time, movie_time


@dataclass
class ClickhouseView:
    user_id: str
    movie_id: str
    views_time: int
    movie_time: int
    event_time: datetime


class Transformer:
    @staticmethod
    def transform(messages: list[KafkaView]) -> list[ClickhouseView]:
        views = []
        for message in messages:
            user_id, movie_id = message.movie_user()
            views_time, movie_time = message.view()
            if user_id is None or movie_id is None or views_time is None or movie_time is None:
                break
            event_time = message.date()
            logger.info('Transformed data {0}, {1}, {2}, {3}, {4}'.format(user_id, movie_id, views_time,
                                                                          movie_time, event_time))
            views.append(ClickhouseView(user_id, movie_id, views_time, movie_time, event_time))
        return views
