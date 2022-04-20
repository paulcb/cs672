#!/bin/sh
docker build -f app_a/Dockerfile -t app_a .
docker run --name app_a_1 -it -v /storage app_a /bin/bash
docker container start app_a_1
docker exec -it app_a_1 bash
docker container rm -f app_a_1

docker run --hostname my-rabbit --network=net1 -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management

docker run --network=net1 --name app_a_1 -it -v /storage app_a /bin/bash

docker run -it --network=net1 --rm --name tensorflow tensorflow/tensorflow