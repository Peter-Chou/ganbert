#!/bin/bash

mkdir /logs

touch /logs/weibo_filter.err.log && touch /logs/weibo_filter.out.log

nohup tensorflow_model_server --port=8500 --rest_api_port=8501 \
      --model_name=ganbert --model_base_path=/saved_model \
      --per_process_gpu_memory_fraction=$GPU_MEMORY_FRACTION \
      --enable_model_warmup=true > tf_serving.log 2>&1 &

# python gateway.py
/usr/bin/supervisord
