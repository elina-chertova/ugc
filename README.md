# UGC service

1. Information about running UGC service: `ugc/README.md`.
2. Notification about `push`: Telegram bot `@UGCservicebot`.
3. Benchmark:  `benchmark/OLAP_research` (ClickHouse vs Vertica), `benchmark/storage` (MongoDB vs ClickHouse).


# Run project

```angular2html
<!--UGC service. Root directory.-->

<!--DB-->
make run_mongo
make run_kafka
make run_clickhouse

<!--ETL+API-->
make run_ugc

<!--ELK-->
make run_elk
```


