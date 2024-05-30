import pandas as pd
from clickhouse_driver import Client

client = Client(host='localhost',
                settings={"use_numpy": True})


df = pd.read_csv('/Users/elinachertova/PycharmProjects/UGC_service/ugc/storage_research/views_data.csv')


query = 'INSERT INTO test.views VALUES'
step = 2

for i in range(0, df.shape[0], step):
    batch = df[i:i+step].copy()
    client.insert_dataframe(query, batch)



