#!/bin/bash

cd /mnt/data/icg27/firmament-experiments/analysis/plotting/
python plot_solver_flip_runtime_cdf.py --trace_paths=/mnt/data/icg27/firmament_simulations/quincy/google_3600_sec_quincy_13pus_solver_flip/,/mnt/data/icg27/firmament_simulations/quincy/google_3600_sec_quincy_13pus_solver_flip_without_refine/ --trace_labels="Price refine + cost scaling,Cost scaling" --paper_mode --log_scale=False --algorithm=cost_scaling

mv algorithm_runtimes_cdf.pdf quincy_cost_scaling_solver_flip_runtimes_cdf.pdf
