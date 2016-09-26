#!/bin/bash

# Task events per time interval
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_trace_plots.sh'

# Arc prioritization
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_octopus_relax_optimizations.sh'

# Task removal
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_quincy_incremental_optimizations.sh'

# Scheduler & Algorithm runtime CDFs for various solvers
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_quincy_pinned_scheduling_runtimes.sh 14400'
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_quincy_preemption_scheduling_runtimes.sh 14400'
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_quincy_algorithms_runtime_cluster_size.sh'

# Quincy scalability
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_quincy_pinned_scalability_cluster.sh 14400'
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_quincy_preemption_scalability_cluster.sh 14400'

# Quincy percentage of migrated tasks
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_quincy_preemption_percentage_migrated_tasks.sh 14400'

# Quincy percentage of evicted tasks
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_quincy_preemption_percentage_evicted_tasks.sh 14400'

# DFS plots
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_dfs_plots.sh 14400'

# Quincy arc preferences
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_quincy_arc_preferences.sh 14400'

# Scheduler backlog timeline
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_quincy_pinned_scheduling_backlog_timeline.sh 14400'
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_quincy_preemption_scheduling_backlog_timeline.sh 14400'

# Num changes vs runtime
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_quincy_pinned_algorithm_runtime_vs_num_changes.sh 14400'
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_quincy_preemption_algorithm_runtime_vs_num_changes.sh 14400'

# Scheduling delay
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_quincy_pinned_scheduling_delay.sh 14400 1'
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_quincy_preemption_scheduling_delay.sh 14400 1'

# Incremental Relax optimizations
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_quincy_incremental_relax_optimizations_runtime.sh 14400'
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_quincy_incremental_relax_timeline.sh 14400'

# Solver flip time
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_quincy_solver_flip_runtime.sh 14400'

# Percentage data locality
# TODO(ionel): Add!

# Copy the PDFs
scp ganymede.cl.cam.ac.uk:/mnt/data/icg27/firmament-experiments/analysis/plotting/*.pdf ./
