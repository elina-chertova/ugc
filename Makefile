#!/bin/bash

run_ugc:
	docker-compose -f ugc/docker-compose.yml up -d

run_mongo:
	docker-compose -f containers/MongoDB/docker-compose.yml up -d
	sleep 150
	bash containers/MongoDB/configuration.sh
	bash containers/MongoDB/database.sh

run_kafka:
	docker-compose -f containers/Kafka/docker-compose.yml up -d

run_clickhouse:
	docker-compose -f containers/ClickHouse/docker-compose.yml up -d

run_elk:
	docker-compose -f ELK/docker-compose.yml up -d



