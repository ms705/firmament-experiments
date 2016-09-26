#!/bin/bash

while [[ $# -ge 1 ]]; do
  key="$1"

  case $key in
      -r|--experiment-root)
      EXPERIMENTS_ROOT="$2"
      shift # past argument
      ;;
      -h|--help)
      echo "usage: ./$(basename $0) [ -r|--experiment-root <path> ]"
      exit 0
      ;;
      *)
      # unknown option
      ;;
  esac
  shift # past argument or value
done

python plot_net_task_duration_cdf.py \
  --trace_paths=${EXPERIMENTS_ROOT}/results/caelum_40_machines_net_cost_model/iperf_21_machines_3_nginx_7_ab_udp_net_cost_model_2x_cpuspin/ \
  --trace_labels='Ideal (isolation),Firmament' \
  --ideal_runtimes_path=${EXPERIMENTS_ROOT}/results/caelum_40_machines_net_cost_model/hdfs_baseline_idle_cluster_time1 \
  --docker_results_file=${EXPERIMENTS_ROOT}/results/caelum_40_machines_net_cost_model/iperf_21_machines_3_nginx_7_ab_udp_docker_2x_cpuspin.csv \
  --kubernetes_results_file=${EXPERIMENTS_ROOT}/results/caelum_40_machines_net_cost_model/iperf_21_machines_3_nginx_7_ab_udp_kubernetes_2x_cpuspin.csv \
  --mesos_log_file=${EXPERIMENTS_ROOT}/results/caelum_40_machines_net_cost_model/iperf_21_machines_3_nginx_7_ab_udp_mesos_2x_cpuspin.log \
  --sparrow_results_file=${EXPERIMENTS_ROOT}/results/caelum_40_machines_net_cost_model/iperf_21_machines_3_nginx_7_ab_udp_sparrow_fifo_2x_cpuspin.csv \
  --paper_mode
mv task_response_time_cdf.pdf net_task_response_time_cdf.pdf

#python plot_net_task_duration_box_whiskers.py \
#  --trace_paths=${EXPERIMENTS_ROOT}/results/caelum_40_machines_net_cost_model/iperf_21_machines_3_nginx_7_ab_udp_net_cost_model_2x_cpuspin/ \
#  --trace_labels='Ideal (isolation),Firmament' \
#  --ideal_runtimes_path=${EXPERIMENTS_ROOT}/results/caelum_40_machines_net_cost_model/hdfs_baseline_idle_cluster_time1 \
#  --docker_results_file=${EXPERIMENTS_ROOT}/results/caelum_40_machines_net_cost_model/iperf_21_machines_3_nginx_7_ab_udp_docker_2x_cpuspin.csv \
#  --kubernetes_results_file=${EXPERIMENTS_ROOT}/results/caelum_40_machines_net_cost_model/iperf_21_machines_3_nginx_7_ab_udp_kubernetes_2x_cpuspin.csv \
#  --mesos_log_file=${EXPERIMENTS_ROOT}/results/caelum_40_machines_net_cost_model/iperf_21_machines_3_nginx_7_ab_udp_mesos_2x_cpuspin.log \
#  --sparrow_results_file=${EXPERIMENTS_ROOT}/results/caelum_40_machines_net_cost_model/iperf_21_machines_3_nginx_7_ab_udp_sparrow_fifo_2x_cpuspin.csv \
#  --paper_mode
#mv net_task_duration_box_whiskers.pdf net_task_response_time_box_whiskers.pdf
