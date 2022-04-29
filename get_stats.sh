#!/bin/bash


rm opt/transactions.txt
rm opt/out.txt
rm opt/transactions.json

python3 rpc_client.py localhost > opt/transactions.txt &
pid1=$!
echo $pid1

# d1=`date "+%H:%M:%S"`
# echo "{\"TIME_START\":\"$d1\"}" >> out.txt
# docker stats --format "{{ json . }}" >> out.txt &
# pid2=$!
# echo $pid2

sleep 30

docker cp cs672-app_a-0-1:/opt/example.db .
docker cp cs672-app_a-0-1:/opt/example.db .

# docker exec -it cs672-tensorflow-1 pkill -f iostat
# docker exec -it cs672-app_a-0-1 pkill -f iostat

# docker cp cs672-tensorflow-1:/opt/out_iostat_tensorflow.txt .
# docker cp cs672-app_a-0-1:/opt/out_iostat_app_a.txt .

kill -15 $pid1

# kill -15 $pid2
# d2=`date "+%H:%M:%S"`
# echo "{\"TIME_END\":\"$d2\"}" >> out.txt
