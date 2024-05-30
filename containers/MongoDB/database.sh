#!/bin/bash

# create database
docker exec -it mongors1n1 bash -c 'echo "use UserMovie" | mongosh'

# enable sharding
docker exec -it mongos1 bash -c 'echo "sh.enableSharding(\"UserMovie\")" | mongosh'

# enable collection
docker exec -it mongos1 bash -c 'echo "db.createCollection(\"UserMovie.UserMovieCollection\")" | mongosh'

# sharding on field
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"UserMovie.UserMovieCollection\", {\"user_id\": \"hashed\"})" | mongosh'



# enable sharding
docker exec -it mongos1 bash -c 'echo "sh.enableSharding(\"Rating\")" | mongosh'

# enable collection
docker exec -it mongos1 bash -c 'echo "db.createCollection(\"Rating.RatingCollection\")" | mongosh'

# sharding on field
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"Rating.RatingCollection\", {\"user_id\": \"hashed\"})" | mongosh'



# enable sharding
docker exec -it mongos1 bash -c 'echo "sh.enableSharding(\"Review\")" | mongosh'

# enable collection
docker exec -it mongos1 bash -c 'echo "db.createCollection(\"Review.ReviewCollection\")" | mongosh'

# sharding on field
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"Review.ReviewCollection\", {\"user_id\": \"hashed\"})" | mongosh'




# enable sharding
docker exec -it mongos1 bash -c 'echo "sh.enableSharding(\"Bookmarks\")" | mongosh'

# enable collection
docker exec -it mongos1 bash -c 'echo "db.createCollection(\"Bookmarks.BookmarksCollection\")" | mongosh'

# sharding on field
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"Bookmarks.BookmarksCollection\", {\"user_id\": \"hashed\"})" | mongosh'

