#!/bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
source ${DIR}/../perf_conf.sh
 
if [ $# -lt 1 ]; then
  echo "usage: perf_helper.sh <command with arguments>"
  exit 1
fi

perf stat -x "," -o cpu_spin.${DURATION}s.${HOSTNAME}${EXPERIMENT}.perf $(for e in ${EVENTS}; do echo -n "-e ${e} "; done) "$@"
