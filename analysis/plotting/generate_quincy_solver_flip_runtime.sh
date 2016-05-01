#!/bin/bash

cd /mnt/data/icg27/firmament-experiments/analysis/plotting/
python plot_solver_flip_runtime_cdf.py --trace_paths=/mnt/data/icg27/firmament_simulations/quincy/google_3600_sec_quincy_13pus_solver_flip_without_refine,/mnt/data/icg27/firmament_simulations/quincy/google_3600_sec_quincy_13pus_solver_flip --trace_labels="cost scaling,cost scaling + price refine" --paper_mode --log_scale=False --algorithm=cost_scaling

mv algorithm_runtimes_cdf-90th.pdf quincy_cost_scaling_solver_flip_runtimes_cdf-90th.pdf
mv algorithm_runtimes_cdf-99th.pdf quincy_cost_scaling_solver_flip_runtimes_cdf-99th.pdf
mv algorithm_runtimes_cdf.pdf quincy_cost_scaling_solver_flip_runtimes_cdf.pdf
