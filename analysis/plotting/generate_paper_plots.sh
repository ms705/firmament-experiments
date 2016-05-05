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

# Approximate algorithms (Figure 9)
ssh ganymede.cl.cam.ac.uk 'python /mnt/data/icg27/firmament-experiments/analysis/plotting/plot_approximate_algorithms.py --input_files=/mnt/data/icg27/firmament-experiments/results/approximate_solvers/approximate_relax_results.csv,/mnt/data/icg27/firmament-experiments/results/approximate_solvers/approximate_cost_scaling_results.csv --labels="Relax,Cost scaling" --paper_mode'

# Arc prioritization (Figure 10)
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_octopus_relax_optimizations.sh'

# Task removal (Figure 11)
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_quincy_incremental_optimizations.sh'

# Solver flipping (Figure 12)
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_quincy_solver_flip_runtime.sh'

# Rapid vs just running relax/cost_scaling at 97% utilization (Figure 13)
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_rapid_recovering_timeline.sh'

# Rapid vs Quincy at 90% utilization (Figure 14)
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_quincy_task_placement.sh'

# Rapid breaking point (Figure 15)
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_rapid_breaking_point.sh'

# Google speedup (Figure 16)
# TODO
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/'

# Percentage data locality (Figure 17)
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_algorithm_runtime_preference_threshold.sh'
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_task_percentage_local_input.sh'


# Quincy machine hogging (Figure 18)
# TODO

# Copy the PDFs
scp ganymede.cl.cam.ac.uk:/mnt/data/icg27/firmament-experiments/analysis/plotting/*.pdf ./
