#!/bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
OUT_DIR=${OUT_DIR:-.}

if [ $# -lt 2 ]; then
  export CONF=client
  SERVER=tigger
else
  export CONF=$1
  SERVER=$2
fi

mkdir -p ${OUT_DIR}

touch ${OUT_DIR}/net_stream.${CONF}.${HOSTNAME}${EXPERIMENT}.out
if [[ ${CONF} == "server" ]]; then
  ${DIR}/perf_helper.sh /usr/bin/time -o ${OUT_DIR}/net_stream.${CONF}.${HOSTNAME}${EXPERIMENT}.time --verbose /usr/bin/iperf -s -o ${OUT_DIR}/io_stream.${CONF}.${HOSTNAME}${EXPERIMENT}.out -i 1
else
  ${DIR}/perf_helper.sh /usr/bin/time -o ${OUT_DIR}/net_stream.${CONF}.${HOSTNAME}${EXPERIMENT}.time --verbose /usr/bin/iperf -c ${SERVER} -o ${OUT_DIR}/io_stream.${CONF}.${HOSTNAME}${EXPERIMENT}.out -i 1 -n 20480M
fi
