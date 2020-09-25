#!/bin/bash
SCRIPT=$(readlink -f "$0")
CUR_DIR=$(dirname "$SCRIPT")
PAR_DIR=$(dirname ${CUR_DIR})

docker-compose -f ${PAR_DIR}/docker-compose.yml --env-file=${PAR_DIR}/compose.env build
