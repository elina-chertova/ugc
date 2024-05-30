-- common
CREATE DATABASE shard;
CREATE DATABASE replica;

-- node 3
CREATE TABLE shard.views (user_id UUID, movie_id UUID, views_time UInt16, movie_time UInt16, event_time DateTime) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/views', 'replica_1') PARTITION BY toYYYYMMDD(event_time) ORDER BY event_time;
CREATE TABLE replica.views (user_id UUID, movie_id UUID, views_time UInt16, movie_time UInt16, event_time DateTime) Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/views', 'replica_2') PARTITION BY toYYYYMMDD(event_time) ORDER BY event_time;
CREATE TABLE default.views (user_id UUID, movie_id UUID, views_time UInt16, movie_time UInt16, event_time DateTime) ENGINE = Distributed('company_cluster', '', views, rand());

