import logging
from functools import lru_cache

from aiokafka import AIOKafkaProducer
from clickhouse_driver import Client
from db.clickhouse import get_clickhouse
from db.kafka import get_producer
from event_source.kafka import KafkaSource
from fastapi import Depends
from models.views import View
from services.utils import BaseViews
from storage.clickhouse import ClickhouseStorage

logger = logging.getLogger(__name__)


class Views(BaseViews):
    def __init__(self, producer, olap_storage):
        self.producer = producer
        self.olap_storage = olap_storage

    @property
    def topic(self) -> str:
        return 'views'

    @staticmethod
    def pagination(lst: list, page_size: int, page: int):
        res = lst[(page - 1) * page_size: page * page_size]
        return res

    async def send_view_info(self, timing: int, user_id: str, movie_id: str, movie_time: int) -> None:
        """
        Отправить данные о просмотре фильма в кафку.
        :param timing:
        :param user_id:
        :param movie_id:
        :param movie_time:
        :return:
        """
        key = '{0}+{1}'.format(movie_id, user_id)
        value = '{0}+{1}'.format(timing, movie_time)
        await self.producer.send(topic=self.topic, event_key=key.encode('utf-8'), event_value=value.encode('utf-8'))
        logger.info('Topic {0} with key {1}, value {2}'.format(self.topic, key, value))

    async def get_history(self, user_id: str, page: int, page_size: int) -> list[View]:
        """
        Получить историю просмотров фильмов с таймингами конкретного пользователя.
        :param user_id:
        :param page:
        :param page_size:
        :return:
        """
        query = "SELECT * FROM default.views WHERE user_id='{0}';".format(user_id)
        views = await self.olap_storage.get(query)

        result = [View(user_id=item[0], movie_id=item[1], view_time=item[2],
                       movie_time=item[3], event_time=item[4]) for item in views]
        paginator = self.pagination(result, page_size, page)
        return paginator


@lru_cache()
def get_views_service(
    producer: AIOKafkaProducer = Depends(get_producer),
    storage: Client = Depends(get_clickhouse)
) -> Views:
    producer = KafkaSource(producer)
    olap_storage = ClickhouseStorage(storage)
    return Views(producer, olap_storage)
