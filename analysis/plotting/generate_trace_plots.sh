#!/bin/bash

python plot_scheduling_events_per_time_interval_cdf.py --trace_path=/data/flowlessly/google_trace/  --num_files_to_process=500 --time_intervals='500000,1000000,2000000,5000000,10000000,20000000' --time_labels='500 ms,1000 ms,2000 ms,5000 ms,10000 ms,20000 ms' --paper_mode

python plot_machine_removals_per_time_interval.py  --trace_path=/data/flowlessly/google_trace/ --time_interval=100000000 --paper_mode
