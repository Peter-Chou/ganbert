# deploy instruction

## build images

### build base image

``` sh
docker build --pull -t weibofilter-base:0.0.0-gpu -f docker/base-gpu.dockerfile ./docker/.
```

### build gateway image

``` sh
docker build --no-cache --build-arg BASE_VERSION=weibofilter-base:0.0.0-gpu \
  -t weibofilter-gateway:0.0.0-gpu -f gateway-gpu.dockerfile .
```

## start serving

``` sh
PORT=34568 GPUS=0 INSTANCES=3 GPU_PCT=0.1  bash -c 'docker run --gpus
  device=$GPUS -p $PORT:9004 -e GATEWAY_INSTANCES=$INSTANCES -e GPU_MEMORY_FRACTION=$GPU_PCT --name weibo_filter_$PORT \
  --mount type=bind,source=$(pwd)/saved_model,target=/saved_model \
  -t weibofilter-gateway:0.0.0-gpu &'


PORT=34568 GPUS=0 bash -c 'docker run --gpus device=$GPUS -p $PORT:9004 \
  --env-file=gateway-gpu.env --name weibofilter_$PORT \
  --mount type=bind,source=$(pwd)/saved_model,target=/saved_model \
  -t weibofilter-gateway:0.0.0-gpu &'
```
