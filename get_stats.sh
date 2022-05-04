#!/bin/bash

# cs672-app_a-0_1
cname1=cs672_app_a-0_1
cname2=cs672_tensorflow_gpu_1
rm opt/*

python3 rpc_client.py localhost > opt/transactions.txt &
pid1=$!
echo $pid1

d1=`date "+%H:%M:%S"`
echo "{\"TIME_START\":\"$d1\"}" > opt/out.txt
docker stats --format "{{ json . }}" >> opt/out.txt &
pid2=$!
# echo $pid2


nvidia-smi -l 1 > opt/foo.txt &
pid3=$!

sleep 120
# docker exec -it cs672-app_a-0-1 pkill -f rpc_server.py
docker cp  $cname1:/opt/example.db opt/
docker cp  $cname1:/opt/transaction_metrics.txt opt/
# docker cp  $cname2:/opt/foo opt/

# docker exec -it cs672-tensorflow-1 pkill -f iostat

# docker cp cs672-tensorflow-1:/opt/out_iostat_tensorflow.txt .
# docker cp cs672-app_a-0-1:/opt/out_iostat_app_a.txt .

kill -15 $pid1

kill -15 $pid2
kill -15 $pid3
d2=`date "+%H:%M:%S"`
echo "{\"TIME_END\":\"$d2\"}" >> opt/out.txt
