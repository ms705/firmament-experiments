#!/bin/bash

python plot_net_task_duration_cdf.py --trace_paths=/mnt/data/icg27/firmament-experiments/results/caelum_40_machines_net_cost_model/net_cost_model_2x_cpuspin_idle/ --trace_labels='Idle,Firmament' --ideal_runtimes_path=/mnt/data/icg27/firmament-experiments/results/caelum_40_machines_net_cost_model/hdfs_baseline_idle_cluster_time1 --docker_results_file=/mnt/data/icg27/firmament-experiments/results/caelum_40_machines_net_cost_model/docker_2x_cpuspin_idle.csv --kubernetes_results_file=/mnt/data/icg27/firmament-experiments/results/caelum_40_machines_net_cost_model/kubernetes_2x_cpuspin_idle.csv --mesos_log_file=/mnt/data/icg27/firmament-experiments/results/caelum_40_machines_net_cost_model/mesos_2x_cpuspin_idle.log --sparrow_results_file=/mnt/data/icg27/firmament-experiments/results/caelum_40_machines_net_cost_model/sparrow_2x_cpuspin_idle.csv --paper_mode
