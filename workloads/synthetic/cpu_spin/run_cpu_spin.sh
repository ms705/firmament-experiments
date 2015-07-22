#!/bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
OUT_DIR=${OUT_DIR:-.}

if [ $# -lt 1 ]; then
  export DURATION=10
else
  export DURATION=$1
fi

mkdir -p ${OUT_DIR}

${DIR}/perf_helper.sh /usr/bin/time -o ${OUT_DIR}/cpu_spin.${DURATION}s.${HOSTNAME}${EXPERIMENT}.time --verbose ${DIR}/cpu_spin ${DURATION} > ${OUT_DIR}/cpu_spin.${DURATION}s.${HOSTNAME}${EXPERIMENT}.out
