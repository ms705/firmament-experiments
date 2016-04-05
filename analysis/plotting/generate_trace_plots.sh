#!/bin/bash

python plot_scheduling_events_per_time_interval_cdf.py --trace_path=/data/flowlessly/google_trace/  --num_files_to_process=500 --time_intervals='500000,750000,1000000,2000000,4000000,6000000,8000000,10000000,20000000' --time_labels='500 ms,750 ms,1000 ms,2000 ms,4000 ms,6000 ms,8000 ms,10000 ms,20000 ms'

python plot_machine_removals_per_time_interval.py  --trace_path=/data/flowlessly/google_trace/ --time_interval=100000000
