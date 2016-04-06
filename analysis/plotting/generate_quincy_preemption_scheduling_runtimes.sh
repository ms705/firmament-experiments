#!/bin/bash
# $1 duration in seconds

cd /mnt/data/icg27/firmament-experiments/analysis/plotting/
python plot_scheduler_runtime_cdf.py --trace_paths=/mnt/data/icg27/firmament_simulations/quincy/google_$1_sec_quincy_preemption_bounded_1024MB_flowlessly_cost_scaling/,/mnt/data/icg27/firmament_simulations/quincy/google_$1_sec_quincy_preemption_bounded_1024MB_flowlessly_incremental_cost_scaling/,/mnt/data/icg27/firmament_simulations/quincy/google_$1_sec_quincy_preemption_bounded_1024MB_flowlessly_relax/,/mnt/data/icg27/firmament_simulations/quincy/google_$1_sec_quincy_preemption_bounded_1024MB_flowlessly_incremental_cost_scaling_then_relax/ --trace_labels="cost scaling,incremental cost scaling,relax,incremental relax" --runtimes_after_timestamp=11078671198
mv scheduling_runtimes_cdf-90th.pdf quincy_$1_sec_bounded_1024MB_preemption_scheduling_runtimes_cdf-90th.pdf
mv scheduling_runtimes_cdf-99th.pdf quincy_$1_sec_bounded_1024MB_preemption_scheduling_runtimes_cdf-99th.pdf
mv scheduling_runtimes_cdf.pdf quincy_$1_sec_bounded_1024MB_preemption_scheduling_runtimes_cdf.pdf
mv algorithm_runtimes_cdf-90th.pdf quincy_$1_sec_bounded_1024MB_preemption_algorithm_runtimes_cdf-90th.pdf
mv algorithm_runtimes_cdf-99th.pdf quincy_$1_sec_bounded_1024MB_preemption_algorithm_runtimes_cdf-99th.pdf
mv algorithm_runtimes_cdf.pdf quincy_$1_sec_bounded_1024MB_preemption_algorithm_runtimes_cdf.pdf