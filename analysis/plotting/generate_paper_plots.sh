#!/bin/bash

# Quincy scalability (Figure 1)
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_quincy_preemption_scalability_cluster.sh'

# Task events per time interval (Figure 2)
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_trace_plots.sh'

# Quincy algorithm runtime (Figure 5)
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_quincy_algorithms_runtime_cluster_size.sh'

# Octopus tasks per second (Figure 6)
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_octopus_algorithm_runtime_tasks_per_round.sh'

# Quincy high cluster utilization (Figure 7)
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_quincy_algorithm_runtime_tasks_per_round.sh'

# Quincy incremental cost scaling (Figure 8)
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_incremental_cost_scaling_runtime_cdf.sh'

# Approximate algorithms (Figure 10)
ssh ganymede.cl.cam.ac.uk 'python /mnt/data/icg27/firmament-experiments/analysis/plotting/plot_approximate_algorithms.py --input_files=/mnt/data/icg27/firmament-experiments/results/approximate_solvers/approximate_relax_results.csv,/mnt/data/icg27/firmament-experiments/results/approximate_solvers/approximate_cost_scaling_results.csv --labels="relax,cost scaling" --paper_mode'

# Arc prioritization (Figure 11)
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/'

# Copy the PDFs
scp ganymede.cl.cam.ac.uk:/mnt/data/icg27/firmament-experiments/analysis/plotting/*.pdf ./
