#!/bin/bash

python3 /opt/rpc_server_tensorflow.py rabbit-0 sleep &
pid1=$!

iostat -x 1 > /opt/out_iostat.txt
