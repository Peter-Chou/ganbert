ARG BASE_VERSION=base:latest

FROM ${BASE_VERSION} as base_image

WORKDIR /weibo_filter

# copy current project to container
COPY . /weibo_filter

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN chmod +x entrypoint.sh

CMD ./entrypoint.sh && tail -f /dev/null
