#!/bin/bash

if [[ $# -lt 2 ]]; then
  echo "usage: start_cluster.sh <host file> <parent coordinator IP> [scheduler] [cost model]"
  exit 1
fi

SCHEDULER=simple
COST_MODEL=""
LOG_DIR=/tmp

if [[ $# -ge 3 ]]; then
  SCHEDULER=$3
fi
if [[ $# -eq 4 ]]; then
  COST_MODEL="--flow_scheduling_cost_model=$4"
fi

# start local coordinator
build/engine/coordinator --listen_uri=tcp:$2:9999 --task_lib_path=/home/srguser/firmament/build/engine/ --scheduler=${SCHEDULER} ${COST_MODEL} --log_dir=${LOG_DIR} --task_log_directory=/home/srguser/firmament-logs/ &
sleep 1

# start other coordinators and link them into local one
parallel-ssh -t 0 -h $1 "cd firmament; build/engine/coordinator --parent_uri=tcp:$2:9999 --task_lib_path=/home/srguser/firmament/build/engine/ --scheduler=${SCHEDULER} ${COST_MODEL} --log_dir=${LOG_DIR} --task_log_directory=/home/srguser/firmament-logs/"
