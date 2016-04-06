#!/bin/bash
# $1 duration in seconds

cd /mnt/data/icg27/firmament-experiments/analysis/plotting/
python plot_scheduling_backlog_timeline.py --trace_paths="/mnt/data/icg27/firmament_simulations/quincy/google_$1_sec_quincy_preemption_bounded_1024MB_flowlessly_incremental_cost_scaling/,/mnt/data/icg27/firmament_simulations/quincy/google_$1_sec_quincy_preemption_bounded_1024MB_flowlessly_incremental_cost_scaling_then_relax/" --trace_labels="incremental cost scaling,incremental relax" --runtimes_after_timestamp=50000000
mv percentage_unscheduled_tasks_timeline.pdf quincy_$1_sec_bounded_1024MB_preemption_percentage_unscheduled_tasks_timeline.pdf
