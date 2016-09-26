#!/bin/bash

function usage() {
  echo "usage: ./$(basename $0) [ -r|--experiment-root <path> ]"
}

while [[ $# -ge 1 ]]; do
  key="$1"

  case $key in
      -r|--experiment-root)
      EXPERIMENTS_ROOT="$2"
      shift # past argument
      ;;
      -h|--help)
      usage
      exit 0
      ;;
      *)
      # unknown option
      ;;
  esac
  shift # past argument or value
done

if [[ ${EXPERIMENTS_ROOT} == "" ]]; then
  usage
  exit 1
fi

python plot_net_task_duration_cdf.py \
  --trace_paths=${EXPERIMENTS_ROOT}/results/caelum_40_machines_net_cost_model/net_cost_model_2x_cpuspin_idle/ \
  --trace_labels='Ideal (isolation),Firmament' \
  --ideal_runtimes_path=${EXPERIMENTS_ROOT}/results/caelum_40_machines_net_cost_model/hdfs_baseline_idle_cluster_time1 \
  --docker_results_file=${EXPERIMENTS_ROOT}/results/caelum_40_machines_net_cost_model/docker_2x_cpuspin_idle.csv \
  --kubernetes_results_file=${EXPERIMENTS_ROOT}/results/caelum_40_machines_net_cost_model/kubernetes_2x_cpuspin_idle.csv \
  --mesos_log_file=${EXPERIMENTS_ROOT}/results/caelum_40_machines_net_cost_model/mesos_2x_cpuspin_idle.log \
  --sparrow_results_file=${EXPERIMENTS_ROOT}/results/caelum_40_machines_net_cost_model/sparrow_2x_cpuspin_idle.csv \
  --xticks_increment=2000000 --paper_mode
mv net_task_duration_box_cdf.pdf net_idle_task_response_time_cdf.pdf
