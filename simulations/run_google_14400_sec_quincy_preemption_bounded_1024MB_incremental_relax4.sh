#!/bin/bash
cd firmament
rm -r /mnt/data/google_14400_sec_quincy_preemption_bounded_1024MB_incremental_relax4/
mkdir /mnt/data/google_14400_sec_quincy_preemption_bounded_1024MB_incremental_relax4/
./build/src/simulator --flagfile=/home/srguser/firmament-experiments/configs/google_14400_sec_quincy_preemption_bounded_1024MB_incremental_relax4.cfg
scp -r /mnt/data/google_14400_sec_quincy_preemption_bounded_1024MB_incremental_relax4/ icg27@ganymede.cl.cam.ac.uk:/mnt/data/icg27/firmament_simulations/
