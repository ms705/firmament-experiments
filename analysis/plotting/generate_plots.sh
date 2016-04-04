#!/bin/bash

# Scheduler & Algorithm runtime CDFs for various solvers
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_quincy_pinned_scheduling_runtimes.sh'

# Quincy scalability
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_quincy_pinned_scalability_cluster.sh'

# Quincy percentage of evicted tasks
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_quincy_pinned_percentage_evicted_tasks.sh'

# DFS plots
ssh ganymede.cl.cam.ac.uk 'cd /mnt/data/icg27/firmament-experiments/analysis/plotting/ ; python plot_dfs_machine_data_cdf.py --trace_path=/mnt/data/icg27/firmament_simulations/old_quincy_pinned/google_14400_sec_quincy_bounded_1024MB_flowlessly_cost_scaling/'

ssh ganymede.cl.cam.ac.uk 'cd /mnt/data/icg27/firmament-experiments/analysis/plotting/ ; python plot_dfs_task_input_data_cdf.py --trace_path=/mnt/data/icg27/firmament_simulations/old_quincy_pinned/google_14400_sec_quincy_bounded_1024MB_flowlessly_cost_scaling/'

ssh ganymede.cl.cam.ac.uk 'cd /mnt/data/icg27/firmament-experiments/analysis/plotting/ ; python plot_input_size_vs_num_arc_preferences.py --trace_path=/mnt/data/icg27/firmament_simulations/old_quincy_pinned/google_14400_sec_quincy_bounded_1024MB_flowlessly_cost_scaling/'

# Copy the pdfs
scp ganymede.cl.cam.ac.uk:/mnt/data/icg27/firmament-experiments/analysis/plotting/*.pdf ./
