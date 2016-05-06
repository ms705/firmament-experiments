#!/bin/bash

if [[ $# -lt 2 ]]; then
  echo "usage: start_cluster.sh <host file> <parent coordinator IP> [scheduler] [cost model]"
  exit 1
fi

SCHEDULER=simple
COST_MODEL=""
LOG_DIR=/tmp
ROOT=/home/srguser

if [[ $# -ge 3 ]]; then
  SCHEDULER=$3
fi
if [[ $# -eq 4 ]]; then
  COST_MODEL="--flow_scheduling_cost_model=$4"
fi

# start local coordinator
build/src/coordinator --listen_uri=tcp:$2:9999 --task_lib_dir=${ROOT}/firmament/build/src/ --scheduler=${SCHEDULER} ${COST_MODEL} --log_dir=${LOG_DIR} --task_log_dir=${ROOT}/firmament-logs/ --task_perf_dir=${ROOT}/firmament-perf --flow_scheduling_solver=cs2 --debug_flow_graph --task_data_dir=/mnt/scratch/ --pin_tasks_to_cores=true --preemption=false --perf_monitoring=false &
sleep 1

# start other coordinators and link them into local one
parallel-ssh -t 0 -h $1 "cd firmament; build/src/coordinator --parent_uri=tcp:$2:9999 --task_lib_dir=${ROOT}/firmament/build/src/ --scheduler=${SCHEDULER} ${COST_MODEL} --flow_scheduling_solver=cs2 --log_dir=${LOG_DIR} --task_log_dir=${ROOT}/firmament-logs/ --task_perf_dir=${ROOT}/firmament-perf --task_data_dir=/mnt/scratch/ --pin_tasks_to_cores=true --preemption=false --perf_monitoring=false"
