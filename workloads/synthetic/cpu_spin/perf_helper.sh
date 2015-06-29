#!/bin/bash
EVENTS="cpu-clock task-clock context-switches cpu-migrations page-faults cycles instructions branches branch-misses mem-loads mem-stores cache-misses cache-references"

if [ $# -lt 1 ]; then
  echo "usage: perf_helper.sh <command with arguments>"
  exit 1
fi

perf stat -x "," -o cpu_spin.${DURATION}s.${HOSTNAME}${EXPERIMENT}.perf $(for e in ${EVENTS}; do echo -n "-e ${e} "; done) "$@"