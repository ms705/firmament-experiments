#!/bin/bash

# Scheduler & Algorithm runtime CDFs for various solvers
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_quincy_pinned_scheduling_runtimes.sh 14400'

# Quincy scalability
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_quincy_pinned_scalability_cluster.sh 14400'

# Quincy percentage of evicted tasks
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_quincy_pinned_percentage_evicted_tasks.sh 14400'

# DFS plots
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_dfs_plots.sh 14400'

# Quincy arc preferences
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_quincy_arc_preferences.sh 14400'

# Scheduler backlog timeline
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_quincy_pinned_scheduling_backlog_timeline.sh 14400'

# Num changes vs runtime
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_quincy_pinned_algorithm_runtime_vs_num_changes.sh 14400'

# Scheduling delay
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_quincy_pinned_scheduling_delay.sh 14400 30'

# Percentage data locality
# TODO(ionel): Add!

# Copy the PDFs
scp ganymede.cl.cam.ac.uk:/mnt/data/icg27/firmament-experiments/analysis/plotting/*.pdf ./
