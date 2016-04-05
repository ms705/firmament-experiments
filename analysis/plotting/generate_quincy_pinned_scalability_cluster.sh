#!/bin/bash

cd /mnt/data/icg27/firmament-experiments/analysis/plotting/
python plot_quincy_scalability.py --trace_paths=/mnt/data/icg27/firmament_simulations/old_quincy_pinned/google_14400_sec_quincy_bounded_1024MB_0.2events_flowlessly_cost_scaling/,/mnt/data/icg27/firmament_simulations/old_quincy_pinned/google_14400_sec_quincy_bounded_1024MB_0.4events_flowlessly_cost_scaling/,/mnt/data/icg27/firmament_simulations/old_quincy_pinned/google_14400_sec_quincy_bounded_1024MB_0.6events_flowlessly_cost_scaling/,/mnt/data/icg27/firmament_simulations/old_quincy_pinned/google_14400_sec_quincy_bounded_1024MB_0.8events_flowlessly_cost_scaling/,/mnt/data/icg27/firmament_simulations/old_quincy_pinned/google_14400_sec_quincy_bounded_1024MB_flowlessly_cost_scaling/ --trace_labels=0.2,0.4,0.6,0.8,1.0 --ignore_runs_before=1

mv quincy_scalability.pdf quincy_4h_pinned_scalability.pdf
