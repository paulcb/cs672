#!/bin/bash

python3 /opt/rpc_server_tensorflow.py rabbit-0 sleep &
pid1=$!

nvidia-smi -l 1 > /opt/foo
