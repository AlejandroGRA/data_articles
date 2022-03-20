#!/bin/sh

docker build -t data_articles .

docker container run --name data_articles -v $(pwd)/data:$(pwd)/data data_articles

#docker container run --name data_articles data_articles # without bind mount
