#!/bin/bash
# $1 firmament log file
grep "TASK BLACKLIST" $1 | grep "cpu_spin" | cut -d' ' -f7 &> blacklisted_tasks.csv
