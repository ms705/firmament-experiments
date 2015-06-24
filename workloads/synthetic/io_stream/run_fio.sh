#!/bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

if [ $# -lt 1 ]; then
  CONF=${DIR}/io_stream/fio-seqwrite.fio
else
  CONF=$1
fi

${DIR}/../perf_helper.sh /usr/bin/fio --output ${CONF}.${HOSTNAME}${EXPERIMENT}.out ${CONF}
