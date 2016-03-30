#!/bin/bash
cd firmament
mkdir /mnt/data/google_14400_sec_quincy_preemption_bounded_1024MB_flowlessly_incremental_relax/
./build/src/simulator --flagfile=/home/srguser/firmament-experiments/configs/google_14400_sec_quincy_preemption_bounded_1024MB_flowlessly_incremental_relax.cfg
