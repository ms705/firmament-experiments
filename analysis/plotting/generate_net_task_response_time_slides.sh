#!/bin/bash

python plot_net_task_duration_cdf_slides.py --trace_paths=/mnt/data/icg27/firmament-experiments/results/caelum_40_machines_net_cost_model/tcp_2sec_between_jobs_iperf_20_machines_3_nginx_7_ab_net_cost_model/,/mnt/data/icg27/firmament-experiments/results/caelum_40_machines_net_cost_model/tcp_2sec_between_jobs_iperf_20_machines_3_nginx_7_ab_simple_random/ --trace_labels='Ideal,Firmament,Random' --ideal_runtimes_path=/mnt/data/icg27/firmament-experiments/results/caelum_40_machines_net_cost_model/hdfs_baselines --paper_mode
