#!/bin/bash
# $1 duration in seconds
# $2 num files to process

cd /mnt/data/icg27/firmament-experiments/analysis/plotting/

python plot_scheduling_delay_cdf.py --num_files_to_process=$2 --trace_paths="/mnt/data/icg27/firmament_simulations/quincy/google_$1_sec_quincy_preemption_bounded_1024MB_flowlessly_cost_scaling/,/mnt/data/icg27/firmament_simulations/quincy/google_$1_sec_quincy_preemption_bounded_1024MB_flowlessly_incremental_cost_scaling/,/mnt/data/icg27/firmament_simulations/quincy/google_$1_sec_quincy_preemption_bounded_1024MB_flowlessly_relax/" --trace_labels="cost scaling,incremental cost scaling,relax"

mv scheduling_delay_cdf.pdf quincy_$1_sec_bounded_1024MB_preemption_scheduling_delay_cdf.pdf
mv scheduling_delay_cdf-90th.pdf quincy_$1_sec_bounded_1024MB_preemption_scheduling_delay_cdf-90th.pdf
mv scheduling_delay_cdf-99th.pdf quincy_$1_sec_bounded_1024MB_preemption_scheduling_delay_cdf-99th.pdf
