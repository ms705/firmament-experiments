#!/bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

if [ $# -lt 1 ]; then
  SIZE=1048576
else
  SIZE=$1
fi

${DIR}/perf_helper.sh ${DIR}/mem_stream ${SIZE} > mem_stream${SIZE}.${HOSTNAME}${EXPERIMENT}.out
