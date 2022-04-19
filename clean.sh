#!/bin/sh
docker stop app_a_1
docker container rm app_a
docker container prune
docker container ls -a