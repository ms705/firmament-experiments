#!/bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

if [ $# -lt 1 ]; then
  DURATION=10
else
  DURATION=$1
fi

${DIR}/perf_helper.sh ${DIR}/cpu_spin ${DURATION} > cpu_spin.${DURATION}s.${HOSTNAME}${EXPERIMENT}.out
