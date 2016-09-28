#!/bin/bash

# Quincy scalability (Figure 2)
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_quincy_preemption_scalability_cluster.sh'

# Quincy algorithm runtime (Figure 6)
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_quincy_algorithms_runtime_cluster_size_slides.sh'

# Quincy high cluster utilization (Figure 7)
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_quincy_algorithm_runtime_tasks_per_round.sh'

# Octopus tasks per second (Figure 8)
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_octopus_algorithm_runtime_tasks_per_round.sh'

# Approximate algorithms (Figure 9)
ssh ganymede.cl.cam.ac.uk 'python /mnt/data/icg27/firmament-experiments/analysis/plotting/plot_approximate_algorithms.py --input_files=/mnt/data/icg27/firmament-experiments/results/approximate_solvers/approximate_relax_results.csv,/mnt/data/icg27/firmament-experiments/results/approximate_solvers/approximate_cost_scaling_results.csv --labels="Relaxation,Cost scaling" --paper_mode'

# Quincy incremental cost scaling (Figure 10)
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_incremental_cost_scaling_runtime_box_and_whiskers.sh'

# Solver optimizations (Figure 12)
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_octopus_relax_optimizations.sh'
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_quincy_incremental_optimizations.sh'

# Solver flipping (Figure 13)
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_quincy_solver_flip_runtime.sh'

# Firmament vs Quincy at 90% utilization (Figure 14)
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_quincy_task_placement.sh'

# Firmament vs just running relax/cost_scaling at 97% utilization (Figure 15)
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_rapid_recovering_timeline.sh'

# Firmament breaking point (Figure 16)
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_rapid_breaking_point.sh'

# Google speedup (Figure 17)
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_google_speedup_box_and_whiskers.sh'

# Percentage data locality (Figure 18)
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_algorithm_runtime_preference_threshold.sh'
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_task_percentage_local_input.sh'

# Firmament vs other schedulers net cost model on idle network (Figure 19)
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_net_idle_task_response_time.sh'

# Firmament vs other schedulers net cost model (Figure 20)
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_net_udp_task_response_time.sh'

# Copy the PDFs
scp ganymede.cl.cam.ac.uk:/mnt/data/icg27/firmament-experiments/analysis/plotting/*.pdf ./
