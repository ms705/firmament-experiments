#!/bin/bash
cd firmament
mkdir /mnt/data/google_14400_sec_quincy_preemption_bounded_1024MB_0.8events_flowlessly_cost_scaling/
./build/src/simulator --flagfile=/home/srguser/firmament-experiments/configs/google_14400_sec_quincy_preemption_bounded_1024MB_0.8events_flowlessly_cost_scaling.cfg
