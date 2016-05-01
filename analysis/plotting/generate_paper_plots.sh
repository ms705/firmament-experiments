#!/bin/bash

# Quincy scalability (Figure 1)
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_quincy_preemption_scalability_cluster.sh'

# Task events per time interval (Figure 2)
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_trace_plots.sh'

# Quincy algorithm runtime (Figure 3)
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_quincy_algorithms_runtime_cluster_size.sh'

# Octopus tasks per second (Figure 4)
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_octopus_algorithm_runtime_tasks_per_round.sh'

# Quincy high cluster utilization (Figure 5)
ssh ganymede.cl.cam.ac.uk '/mnt/data/icg27/firmament-experiments/analysis/plotting/generate_quincy_algorithm_runtime_tasks_per_round.sh'

# Copy the PDFs
scp ganymede.cl.cam.ac.uk:/mnt/data/icg27/firmament-experiments/analysis/plotting/*.pdf ./
