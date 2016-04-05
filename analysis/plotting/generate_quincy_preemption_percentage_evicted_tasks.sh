#!/bin/bash
# $1 duration in seconds

cd /mnt/data/icg27/firmament-experiments/analysis/plotting/
python plot_percentage_evicted_tasks.py --trace_paths="/mnt/data/icg27/firmament_simulations/quincy/google_$1_sec_quincy_preemption_bounded_1024MB_flowlessly_cost_scaling/,/mnt/data/icg27/firmament_simulations/quincy/google_$1_sec_quincy_preemption_bounded_1024MB_flowlessly_incremental_cost_scaling/,/mnt/data/icg27/firmament_simulations/quincy/google_$1_sec_quincy_preemption_bounded_1024MB_flowlessly_relax/,/mnt/data/icg27/firmament_simulations/quincy/google_$1_sec_quincy_preemption_bounded_1024MB_flowlessly_incremental_cost_scaling_then_relax/" --trace_labels="cost scaling,incremental cost scaling,relax,incremental relax"
mv percentage_evicted_tasks_cdf.pdf quincy_$1_sec_bounded_1024MB_preemption_percentage_evicted_tasks.pdf
