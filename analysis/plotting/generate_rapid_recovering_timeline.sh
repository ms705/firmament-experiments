#!/bin/bash

cd /mnt/data/icg27/firmament-experiments/analysis/plotting/

python plot_rapid_recovering_timeline.py --trace_paths=/mnt/data/icg27/firmament_simulations/quincy/google_86400_sec_12pus_quincy_preemption_bounded_1024MB_flowlessly_relax/,/mnt/data/icg27/firmament_simulations/quincy/google_86400_sec_12pus_quincy_preemption_bounded_1024MB_flowlessly_cost_scaling/,/mnt/data/icg27/firmament_simulations/quincy/google_86400_sec_12pus_quincy_preemption_bounded_1024MB_rapid/ --trace_labels='Relaxation only,Cost scaling (Quincy),Firmament' --runtimes_after_timestamp=1000000000 --runtimes_before_timestamp=4000000000 --paper_mode
