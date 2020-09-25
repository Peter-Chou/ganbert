
#!/bin/bash
SCRIPT=$(readlink -f "$0")
CUR_DIR=$(dirname "$SCRIPT")
PAR_DIR=$(dirname ${CUR_DIR})

# usage: ./docker/stop_weibo_gateway.sh port_ip
docker-compose --compatibility -f ${PAR_DIR}/docker-compose.yml --env-file=${PAR_DIR}/compose.env -p weibo_filter_$1 down
