#!/bin/bash
cd firmament
mkdir /mnt/data/google_14400_sec_quincy_preemption_bounded_1024MB_incremental_relax4/
./build/src/simulator --flagfile=/home/srguser/firmament-experiments/configs/google_14400_sec_quincy_preemption_bounded_1024MB_incremental_relax4.cfg
