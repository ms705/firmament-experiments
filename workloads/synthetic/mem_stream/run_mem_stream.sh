#!/bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
OUT_DIR=${OUT_DIR:-.}

if [ $# -lt 1 ]; then
  export SIZE=1048576
else
  export SIZE=$1
fi

mkdir -p ${OUT_DIR}

${DIR}/perf_helper.sh /usr/bin/time -o ${OUT_DIR}/mem_stream.${SIZE}B.${HOSTNAME}${EXPERIMENT}.time --verbose ${DIR}/mem_stream ${SIZE} > ${OUT_DIR}/mem_stream.${SIZE}B.${HOSTNAME}${EXPERIMENT}.out
