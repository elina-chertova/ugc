from core.config import Settings
from storage.base import Storage

conf = Settings()


class ClickhouseStorage(Storage):
    def __init__(self, storage):
        self.storage = storage

    async def get(self, query: str):
        """
        Get data from ClickHouse.
        :param query: SQL query
        :return:
        """
        async with self.storage.cursor() as cursor:
            await cursor.execute(query)
            views = await cursor.fetchall()
        return views

