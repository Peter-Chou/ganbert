ARG BASE_VERSION=base-gpu:latest

FROM ${BASE_VERSION} as base_image

WORKDIR /weibo_filter

# copy current project to container
COPY . /weibo_filter

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN chmod +x entrypoint-gpu.sh

CMD ./entrypoint-gpu.sh && tail -f /dev/null
