#!/bin/bash

# Continuously update the file with the temperature every few seconds
while true; do
    temperature=$(nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader,nounits)
    echo "$temperature""000" > /tmp/gpu_temp
    sleep 5
done
