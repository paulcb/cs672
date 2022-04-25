#!/bin/sh

python3 rpc_client.py localhost > transactions.txt &

d1=`date "+%H:%M:%S"`
echo "{\"TIME_START\":\"$d1\"}" > out.txt
docker stats --format "{{ json . }}" >> out.txt
d2=`date "+%H:%M:%S"`
echo "{\"TIME_END\":\"$d2\"}" >> out.txt
