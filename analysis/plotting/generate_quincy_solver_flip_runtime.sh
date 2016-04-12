#!/bin/bash
# $1 duration in seconds

cd /mnt/data/icg27/firmament-experiments/analysis/plotting/
python plot_solver_flip_runtime_cdf.py --trace_paths=/mnt/data/icg27/firmament_simulations/quincy/google_$1_sec_quincy_preemption_bounded_1024MB_solver_flip_without_refine,/mnt/data/icg27/firmament_simulations/quincy/google_$1_sec_quincy_preemption_bounded_1024MB_solver_flip --trace_labels="solver flip,solver flip + price refine" --paper_mode

mv scheduling_runtimes_cdf-90th.pdf quincy_solver_flip_scheduling_runtimes_cdf-90th.pdf
mv scheduling_runtimes_cdf-99th.pdf quincy_solver_flip_scheduling_runtimes_cdf-99th.pdf
mv scheduling_runtimes_cdf.pdf quincy_solver_flip_scheduling_runtimes_cdf.pdf
mv algorithm_runtimes_cdf-90th.pdf quincy_solver_flip_runtimes_cdf-90th.pdf
mv algorithm_runtimes_cdf-99th.pdf quincy_solver_flip_runtimes_cdf-99th.pdf
mv algorithm_runtimes_cdf.pdf quincy_solver_flip_runtimes_cdf.pdf
