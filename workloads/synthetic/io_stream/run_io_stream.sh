#!/bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

if [ $# -lt 1 ]; then
  CONF=fio-seqwrite.fio
else
  CONF=$1
fi

touch io_stream.${CONF}.${HOSTNAME}${EXPERIMENT}.out
${DIR}/perf_helper.sh /usr/bin/fio --output=io_stream.${CONF}.${HOSTNAME}${EXPERIMENT}.out ${DIR}/${CONF}
