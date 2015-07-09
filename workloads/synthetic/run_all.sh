#!/bin/bash
ITER=9
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

# CPU SPIN
for i in `seq 0 ${ITER}`; do
  echo "CPU spin, run ${i}..."
  export DURATION=60;
  export EXPERIMENT="-baseline-${i}"; 
  ${DIR}/cpu_spin/run_cpu_spin.sh 60;
done

# MEM STREAM
for s in 1024 131072 1048576 52428800; do
  for i in `seq 0 ${ITER}`; do
    echo "mem stream/${s}, run ${i}..."
    export SIZE=${s};
    export EXPERIMENT="-baseline-${i}"; 
    ${DIR}/mem_stream/run_mem_stream.sh ${s};
  done
done

# IO STREAM
for s in fio-seqread.fio fio-seqwrite.fio; do
  for i in `seq 0 ${ITER}`; do
    echo "I/O stream/${s}, run ${i}..."
    export CONF=${s};
    export EXPERIMENT="-baseline-${i}"; 
    ${DIR}/io_stream/run_io_stream.sh ${s};
  done
done
