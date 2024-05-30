from dataclasses import astuple

from clickhouse_driver import Client, errors
from transformer import ClickhouseView
from utils.backoff import backoff
from utils.settings import Settings, logger

settings = Settings()


class Clickhouse:
    def __init__(self, host=settings.clickhouse_host):
        self.host: str = host
        self.connector = self.storage_connector()

    def storage_connector(self):
        return Client(host=self.host)

    @backoff()
    def load(self, views: list[ClickhouseView]) -> bool:
        """
        Загрузка в кликхаус.
        :param views: Список датакласса для загрузки данных в кликхаус.
        :return:
        """
        user_view: list[tuple] = list(map(astuple, views))
        query: str = "INSERT INTO default.views VALUES"
        try:
            self.connector.execute(query, user_view)
        except errors.CannotParseUuidError as e:
            logger.info('Loading error {0}'.format(e))
        logger.info('Data was sent into Clickhouse. Size {0}'.format(len(user_view)))
        logger.info('Variables messages and real_batch were changed.')
        return True


