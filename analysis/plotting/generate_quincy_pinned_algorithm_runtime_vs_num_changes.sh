#!/bin/bash
# $1 duration in seconds

cd /mnt/data/icg27/firmament-experiments/analysis/plotting/
python plot_algo_runtime_vs_num_changes.py --trace_paths=/mnt/data/icg27/firmament_simulations/quincy/google_$1_sec_quincy_bounded_1024MB_flowlessly_incremental_cost_scaling_then_relax/ --trace_labels="incremental relax"
mv algorithm_runtime_vs_num_changes.pdf quincy_$1_sec_bounded_1024MB_pinned_algorithm_runtime_vs_num_changes.pdf
