#!/bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

if [ $# -lt 1 ]; then
  SIZE=1048576
else
  SIZE=$1
fi

${DIR}/perf_helper.sh /usr/bin/time -o mem_stream.${DURATION}s.${HOSTNAME}${EXPERIMENT}.time --verbose ${DIR}/mem_stream ${SIZE} > mem_stream.${SIZE}B.${HOSTNAME}${EXPERIMENT}.out
