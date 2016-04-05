#!/bin/bash
# $1 duration in seconds

cd /mnt/data/icg27/firmament-experiments/analysis/plotting/
python plot_quincy_arc_preferences_cdf.py --trace_path=/mnt/data/icg27/firmament_simulations/quincy/google_$1_sec_quincy_bounded_1024MB_flowlessly_cost_scaling/
mv quincy_arc_preferences_cdf.pdf quincy_$1_sec_bounded_1024MB_pinned_10percent_threshold_arc_preferences_cdf.pdf
