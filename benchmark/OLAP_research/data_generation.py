import datetime
import random
import uuid

import pandas as pd


def generator() -> None:
    """
    Data generator
    :return:
    """
    data_size = 10000000

    df = pd.DataFrame({
        'id': [i for i in range(data_size)],
        'user_id': [uuid.uuid4() for _ in range(data_size)],
        'movie_id': [uuid.uuid4() for _ in range(data_size)],
        'views_time': [random.randint(1, 36000) for _ in range(data_size)],
        'movie_time': [random.randint(1, 36000) for _ in range(data_size)],
        'event_time': [datetime.datetime.today() for _ in range(data_size)]}, dtype=object)

    df.to_csv('views_data.csv')


if __name__ == '__main__':
    generator()

