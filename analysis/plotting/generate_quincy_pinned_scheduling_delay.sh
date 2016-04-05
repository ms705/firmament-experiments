#!/bin/bash
# $1 duration in seconds
# $2 num files to process

cd /mnt/data/icg27/firmament-experiments/analysis/plotting/

python plot_scheduling_delay_cdf.py --num_files_to_process=$2 --trace_paths="/mnt/data/icg27/firmament_simulations/quincy/google_$1_sec_quincy_bounded_1024MB_flowlessly_cost_scaling/,/mnt/data/icg27/firmament_simulations/quincy/google_$1_sec_quincy_bounded_1024MB_flowlessly_incremental_cost_scaling/,/mnt/data/icg27/firmament_simulations/quincy/google_$1_sec_quincy_bounded_1024MB_flowlessly_relax/,/mnt/data/icg27/firmament_simulations/quincy/google_$1_sec_quincy_bounded_1024MB_flowlessly_incremental_cost_scaling_then_relax/" --trace_labels="cost scaling,incremental cost scaling,relax,incremental relax"

mv scheduling_delays_cdf.pdf quincy_$1_sec_bounded_1024MB_pinned_scheduling_delays_cdf.pdf
