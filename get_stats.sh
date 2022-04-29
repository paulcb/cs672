#!/bin/bash


rm transactions.txt
rm out.txt

python3 rpc_client.py localhost > transactions.txt &
pid1=$!
echo $pid1
d1=`date "+%H:%M:%S"`
echo "{\"TIME_START\":\"$d1\"}" >> out.txt
docker stats --format "{{ json . }}" >> out.txt &
pid2=$!
echo $pid2
sleep 120
docker cp cs672_app_a-0_1:/opt/example.db .
kill -15 $pid1
# pkill -f rpc_client.py
kill -15 $pid2
d2=`date "+%H:%M:%S"`
echo "{\"TIME_END\":\"$d2\"}" >> out.txt


