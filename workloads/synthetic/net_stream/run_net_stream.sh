#!/bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

if [ $# -lt 2 ]; then
  CONF=client
  SERVER=tigger
else
  CONF=$1
  SERVER=$2
fi

touch net_stream.${CONF}.${HOSTNAME}${EXPERIMENT}.out
${DIR}/perf_helper.sh /usr/bin/time -o net_stream.${CONF}.${HOSTNAME}${EXPERIMENT}.time --verbose /usr/bin/iperf -c ${SERVER} -o io_stream.${CONF}.${HOSTNAME}${EXPERIMENT}.out -i 1 -n 20480M
