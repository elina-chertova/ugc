import time
from functools import wraps

from clickhouse_driver import errors
from utils.settings import logger


def backoff(log=logger, start_sleep_time: object = 0.5, factor: object = 2,
            border_sleep_time: object = 10) -> object:
    """
    Выполнение функции повторно через некоторое время в случае возникновения ошибки.
    Использует наивный экспоненциальный рост времени повтора (factor) до граничного времени ожидания
    (border_sleep_time)
    Формула:
        t = start_sleep_time * 2^(n) if t < border_sleep_time
        t = border_sleep_time if t >= border_sleep_time
    :param log: логгер
    :param start_sleep_time: начальное время повтора
    :param factor: во сколько раз нужно увеличить время ожидания
    :param border_sleep_time: граничное время ожидания
    :return: результат выполнения функции
    """

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            sleep_time = start_sleep_time
            cnt = 0
            max_tries = 5
            while True:
                try:
                    return func(*args, **kwargs)
                except errors.NetworkError as e:
                    log.error('Connection refused during insert data into Clickhouse')
                except Exception as e:
                    log.error('Connection error: {}'.format(func.__name__), e)

                sleep_time = sleep_time * factor if sleep_time < border_sleep_time else border_sleep_time
                cnt += 1
                time.sleep(sleep_time)
                log.info('Next retries in {0} sec.'.format(sleep_time))

                if cnt > max_tries:
                    log.error(f"Tries were finished {func.__name__}")
                    break

        return inner
    return func_wrapper
