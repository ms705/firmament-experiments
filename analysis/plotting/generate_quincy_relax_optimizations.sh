#!/bin/bash

cd /mnt/data/icg27/firmament-experiments/analysis/plotting/
python plot_relax_optimizations_cdf.py --trace_paths=/mnt/data/icg27/firmament_simulations/quincy/google_14400_sec_95_utilization_quincy_preemption_bounded_1024MB_flowlessly_relax/,/mnt/data/icg27/firmament_simulations/quincy/google_14400_sec_95_utilization_quincy_preemption_bounded_1024MB_flowlessly_relax_without_arc_priority/ --trace_labels="relax arc prioritization,relax" --runtimes_after_timestamp=1000000 --log_scale=True --paper_mode
