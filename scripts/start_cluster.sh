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
build/src/coordinator --listen_uri=tcp:$2:9999 --task_lib_dir=${ROOT}/firmament/build/src/ --scheduler=${SCHEDULER} ${COST_MODEL} --log_dir=${LOG_DIR} --task_log_dir=${ROOT}/firmament-logs/ --task_perf_dir=${ROOT}/firmament-perf --flow_scheduling_solver=cs2 --debug_flow_graph --task_data_dir=/mnt/scratch/ --pin_tasks_to_cores=false --preemption=false --hdfs_name_node_address=hdfs://caelum10g-301.cl.cam.ac.uk --perf_monitoring=false --health_monitor_enable=false --quincy_no_scheduling_delay --monitor_netif=p1p1 --heartbeat_interval=25000 --logtostderr --generate_trace --generated_trace_path=/mnt/data/caelum_40_machines/ --randomly_place_tasks=false &
sleep 3

# start other coordinators and link them into local one
parallel-ssh -t 0 -h ~/caelum-400 -i "cd firmament; build/src/coordinator --parent_uri=tcp:$2:9999 --task_lib_dir=${ROOT}/firmament/build/src/ --scheduler=simple --log_dir=${LOG_DIR} --task_log_dir=${ROOT}/firmament-logs/ --task_perf_dir=${ROOT}/firmament-perf --task_data_dir=/mnt/scratch/ --pin_tasks_to_cores=false --preemption=false --hdfs_name_node_address=hdfs://caelum10g-301.cl.cam.ac.uk --heartbeat_interval=25000 --health_monitor_enable=false --perf_monitoring=false --monitor_netif=p1p1" --randomly_place_tasks=false &
sleep 2
parallel-ssh -t 0 -h ~/caelum-300 -i "cd firmament; build/src/coordinator --parent_uri=tcp:$2:9999 --task_lib_dir=${ROOT}/firmament/build/src/ --scheduler=simple --log_dir=${LOG_DIR} --task_log_dir=${ROOT}/firmament-logs/ --task_perf_dir=${ROOT}/firmament-perf --task_data_dir=/mnt/scratch/ --pin_tasks_to_cores=false --preemption=false --hdfs_name_node_address=hdfs://caelum10g-301.cl.cam.ac.uk --heartbeat_interval=25000 --health_monitor_enable=false --perf_monitoring=false --monitor_netif=p1p1" --randomly_place_tasks=false &
sleep 2
parallel-ssh -t 0 -h ~/caelum-100 -i "cd firmament; build/src/coordinator --parent_uri=tcp:$2:9999 --task_lib_dir=${ROOT}/firmament/build/src/ --scheduler=simple --log_dir=${LOG_DIR} --task_log_dir=${ROOT}/firmament-logs/ --task_perf_dir=${ROOT}/firmament-perf --task_data_dir=/mnt/scratch/ --pin_tasks_to_cores=false --preemption=false --hdfs_name_node_address=hdfs://caelum10g-301.cl.cam.ac.uk --heartbeat_interval=25000 --health_monitor_enable=false --perf_monitoring=false --monitor_netif=p1p1" --randomly_place_tasks=false &
sleep 2
parallel-ssh -t 0 -h ~/caelum-200 -i "cd firmament; build/src/coordinator --parent_uri=tcp:$2:9999 --task_lib_dir=${ROOT}/firmament/build/src/ --scheduler=simple --log_dir=${LOG_DIR} --task_log_dir=${ROOT}/firmament-logs/ --task_perf_dir=${ROOT}/firmament-perf --task_data_dir=/mnt/scratch/ --pin_tasks_to_cores=false --preemption=false --hdfs_name_node_address=hdfs://caelum10g-301.cl.cam.ac.uk --health_monitor_enable=false --heartbeat_interval=25000 --perf_monitoring=false --monitor_netif=p1p1" --randomly_place_tasks=false &
