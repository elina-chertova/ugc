"""Class for Kafka."""
from core.config import Settings
from event_source.base import EventSource

conf = Settings()


class KafkaSource(EventSource):
    def __init__(self, producer):
        self.producer = producer

    async def send(self, topic: str, event_key: str, event_value: str) -> None:
        """
        Send event to Kafka.
        :param topic:
        :param event_key:
        :param event_value:
        :return:
        """
        await self.producer.send_and_wait(topic, key=event_key, value=event_value)
