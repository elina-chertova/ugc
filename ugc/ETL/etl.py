from extractor import KafkaProcess
from kafka import KafkaConsumer
from loader import Clickhouse
from transformer import KafkaView, Transformer
from utils.settings import Settings, logger

settings = Settings()


def etl():
    extractor = KafkaProcess(topic=settings.topic)
    consumer: KafkaConsumer = extractor.consumer_connector()
    transformer = Transformer()
    loader = Clickhouse()

    real_batch: int = 0
    messages: list = []
    for msg in consumer:
        messages.append(KafkaView(msg.key, msg.value, int(msg.timestamp)))
        real_batch += 1
        logger.info('Message in batch, number {0}'.format(real_batch))
        if real_batch >= settings.batch_size:
            views = transformer.transform(messages)
            is_true = loader.load(views)
            if is_true:
                real_batch = 0
                messages = []


etl()
