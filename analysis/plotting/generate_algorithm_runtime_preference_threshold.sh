#!/bin/bash

cd /mnt/data/icg27/firmament-experiments/analysis/plotting/
python plot_algorithm_runtime_threshold_cdf.py --trace_paths=/mnt/data/icg27/firmament_simulations/quincy/google_86400_sec_13pus_quincy_preemption_bounded_1024MB_flowlessly_cost_scaling_2percent_data_threshold/,/mnt/data/icg27/firmament_simulations/quincy/google_86400_sec_13pus_quincy_preemption_bounded_1024MB_flowlessly_cost_scaling_14percent_data_threshold/,/mnt/data/icg27/firmament_simulations/google_86400_sec_13pus_quincy_preemption_bounded_1024MB_rapid_2percent_data_threshold/,/mnt/data/icg27/firmament_simulations/google_86400_sec_13pus_quincy_preemption_bounded_1024MB_rapid_14percent_data_threshold/ --trace_labels='Quincy 2\%,Quincy 14\%,Rapid 2\%,Rapid 14\%' --runtimes_after_timestamp=1000000 --paper_mode
