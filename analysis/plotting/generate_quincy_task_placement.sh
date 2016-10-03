#!/bin/bash

cd /mnt/data/icg27/firmament-experiments/analysis/plotting/
python plot_placement_delay_cdf.py --trace_paths=/mnt/data/icg27/firmament_simulations/quincy_zero_delay/google_86400_sec_13pus_quincy_preemption_bounded_1024MB_rapid_no_delay/,/mnt/data/icg27/firmament_simulations/quincy_zero_delay/google_86400_sec_13pus_quincy_preemption_bounded_1024MB_flowlessly_cost_scaling_no_delay/ --trace_labels='Firmament,Cost scaling (Quincy)' --runtimes_after_timestamp=1000000 --runtimes_before_timestamp=18000000000 --paper_mode

mv scheduling_delay_cdf-90th.pdf quincy_task_placement_cdf-90th.pdf
mv scheduling_delay_cdf-99th.pdf quincy_task_placement_cdf-99th.pdf
mv scheduling_delay_cdf.pdf quincy_task_placement_cdf.pdf
