#!/bin/bash

while true; do
    temperature=$(nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader)
    echo "$temperature""000" > /tmp/gpu_temp
    sleep 5
done
