#!/bin/bash

python plot_google_speedup_relax_runtime_cdf.py --trace_paths=/mnt/data/icg27/firmament_simulations/quincy/google_86400_sec_13pus_quincy_preemption_bounded_1024MB_flowlessly_relax/,/mnt/data/icg27/firmament_simulations/quincy/speedup_experiments/google_4x_speedup_13pus_86400_sec_quincy_preemption_bounded_1024MB_flowlessly_relax/ --trace_labels='1x,4x' --runtimes_after_timestamp=10000000 --paper_mode --time_unit=sec --log_scale=True

#python plot_google_speedup_relax_runtime_cdf.py --trace_paths=/mnt/data/icg27/firmament_simulations/quincy/google_86400_sec_13pus_quincy_preemption_bounded_1024MB_flowlessly_relax/,/mnt/data/icg27/firmament_simulations/quincy/speedup_experiments/google_10x_speedup_13pus_86400_sec_quincy_preemption_bounded_1024MB_flowlessly_relax/,/mnt/data/icg27/firmament_simulations/quincy/speedup_experiments/google_20x_speedup_13pus_86400_sec_quincy_preemption_bounded_1024MB_flowlessly_relax/,/mnt/data/icg27/firmament_simulations/quincy/speedup_experiments/google_40x_speedup_13pus_86400_sec_quincy_preemption_bounded_1024MB_flowlessly_relax/ --trace_labels='1x,10x,20x,40x' --runtimes_after_timestamp=10000000 --paper_mode --time_unit=sec --log_scale=False
mv google_speedup_runtime_cdf.pdf google_speedup_runtime_relax_cdf.pdf