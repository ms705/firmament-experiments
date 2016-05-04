#!/bin/bash

cd /mnt/data/icg27/firmament-experiments/analysis/plotting/
python plot_incremental_optimizations.py --trace_paths=/mnt/data/icg27/firmament_simulations/quincy/google_14400_sec_95_utilization_quincy_preemption_bounded_1024MB_flowlessly_incremental_cost_scaling_without_task_removal/,/mnt/data/icg27/firmament_simulations/quincy/google_14400_sec_95_utilization_quincy_preemption_bounded_1024MB_flowlessly_incremental_cost_scaling/ --trace_labels="cost scaling,cost scaling + task removal" --runtimes_after_timestamp=1000000 --paper_mode