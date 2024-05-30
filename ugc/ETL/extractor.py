from time import sleep

from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import KafkaConnectionError, NoBrokersAvailable
from utils.settings import Settings, logger

settings = Settings()


class KafkaProcess:
    def __init__(self, topic: str):
        self.topic: str = topic
        self.connector: str = '{0}:{1}'.format(settings.kafka_host, settings.kafka_port)
        self.producer = self.producer_connector()
        self.consumer = self.consumer_connector()

    def consumer_connector(self):
        return KafkaConsumer(self.topic, bootstrap_servers=[self.connector],
                             auto_offset_reset='earliest',
                             api_version=(0, 11, 5),
                             group_id='echo-messages-to-stdout',
                             value_deserializer=lambda v: v.decode("utf-8"),
                             key_deserializer=lambda k: k.decode("utf-8"))

    def producer_connector(self):
        return KafkaProducer(security_protocol = "SSL", bootstrap_servers=self.connector,
                             api_version=(0, 11, 5),
                             value_serializer=str.encode,
                             key_serializer=str.encode)

    def get_data(self, value: str, key: str) -> None:
        """
        Функия для загрузки данных в кафку.
        :param value:
        :param key:
        :return:
        """
        try:
            self.producer.send(topic=self.topic, value=value, key=key)
            sleep(1)
        except KafkaConnectionError as e:
            logger.info("Can't send data with value={1}, key={2} to Kafka. Reason: {0}".format(e, value, key))
        except NoBrokersAvailable as e:
            logger.info("Can't send data with value={1}, key={2} to Kafka. Reason: {0}".format(e, value, key))

