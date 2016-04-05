#!/bin/bash
# $1 duration in seconds

cd /mnt/data/icg27/firmament-experiments/analysis/plotting/

# CDF of data per machine
python plot_dfs_machine_data_cdf.py --trace_path=/mnt/data/icg27/firmament_simulations/quincy/google_$1_sec_quincy_bounded_1024MB_flowlessly_cost_scaling/
mv dfs_machine_data_cdf.pdf dfs_$1_sec_bounded_1024MB_machine_data_cdf.pdf

# CDF of input data per task
python plot_dfs_task_input_data_cdf.py --trace_path=/mnt/data/icg27/firmament_simulations/quincy/google_$1_sec_quincy_bounded_1024MB_flowlessly_cost_scaling/
mv dfs_task_input_data_cdf.pdf dfs_$1_sec_bounded_1024MB_task_input_data_cdf.pdf

# Scatter plot of input size versus number of arc preferences
python plot_input_size_vs_num_arc_preferences.py --trace_path=/mnt/data/icg27/firmament_simulations/quincy/google_$1_sec_quincy_bounded_1024MB_flowlessly_cost_scaling/
mv input_size_vs_num_arc_preferences.pdf quincy_$1_sec_bounded_1024MB_pinned_10percent_threshold_input_size_vs_num_arc_preferences.pdf
