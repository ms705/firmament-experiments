#!/bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
OUT_DIR=${OUT_DIR:-.}

if [ $# -lt 1 ]; then
  export CONF=fio-seqwrite.fio
else
  export CONF=$1
fi

mkdir -p ${OUT_DIR}

touch ${OUT_DIR}/io_stream.${CONF}.${HOSTNAME}${EXPERIMENT}.out
${DIR}/perf_helper.sh /usr/bin/time -o ${OUT_DIR}/io_stream.${CONF}.${HOSTNAME}${EXPERIMENT}.time --verbose /usr/bin/fio --output=${OUT_DIR}/io_stream.${CONF}.${HOSTNAME}${EXPERIMENT}.out ${DIR}/${CONF}
