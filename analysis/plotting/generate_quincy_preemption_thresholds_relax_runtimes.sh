#!/bin/bash
# $1 duration in seconds

cd /mnt/data/icg27/firmament-experiments/analysis/plotting/
python plot_scheduler_runtime_cdf.py --trace_paths=/mnt/data/icg27/firmament_simulations/quincy/google_$1_sec_quincy_preemption_bounded_1024MB_flowlessly_relax_1percent_data_threshold/,/mnt/data/icg27/firmament_simulations/quincy/google_$1_sec_quincy_preemption_bounded_1024MB_flowlessly_relax_19percent_data_threshold/,/mnt/data/icg27/firmament_simulations/quincy/google_$1_sec_quincy_preemption_bounded_1024MB_flowlessly_relax_50percent_data_threshold/ --trace_labels="1\%,19\%,50\%" --runtimes_after_timestamp=650000000
mv algorithm_runtimes_cdf-90th.pdf quincy_$1_sec_bounded_1024MB_preemption_thresholds_relax_cdf-90th.pdf
mv algorithm_runtimes_cdf-99th.pdf quincy_$1_sec_bounded_1024MB_preemption_thresholds_relax_cdf-99th.pdf
mv algorithm_runtimes_cdf.pdf quincy_$1_sec_bounded_1024MB_preemption_thresholds_relax_cdf.pdf
