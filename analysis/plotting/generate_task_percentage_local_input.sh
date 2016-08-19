#!/bin/bash

cd /mnt/data/icg27/firmament-experiments/analysis/plotting/

python plot_task_percentage_local_input_cdf.py --trace_paths=/mnt/data/icg27/firmament_simulations/quincy/google_86400_sec_13pus_quincy_preemption_bounded_1024MB_flowlessly_cost_scaling_14percent_data_threshold/,/mnt/data/icg27/firmament_simulations/quincy/google_86400_sec_13pus_quincy_preemption_bounded_1024MB_rapid_2percent_data_threshold/ --trace_labels='Quincy 14\%,Firmament 2\%' --runtimes_after_timestamp=1000000 --runtimes_before_timestamp=8000000000 --paper_mode

python plot_task_percentage_bar_chart.py --trace_paths=/mnt/data/icg27/firmament_simulations/quincy/google_86400_sec_13pus_quincy_preemption_bounded_1024MB_flowlessly_cost_scaling_14percent_data_threshold/,/mnt/data/icg27/firmament_simulations/quincy/google_86400_sec_13pus_quincy_preemption_bounded_1024MB_rapid_2percent_data_threshold/ --trace_labels='Quincy 14\%,Firmament 2\%' --runtimes_after_timestamp=1000000 --runtimes_before_timestamp=8000000000 --paper_mode
