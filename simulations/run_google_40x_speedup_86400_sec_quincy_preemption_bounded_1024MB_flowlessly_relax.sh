#!/bin/bash
cd firmament
rm -r /mnt/data/google_40x_speedup_86400_sec_quincy_preemption_bounded_1024MB_flowlessly_relax/
mkdir /mnt/data/google_40x_speedup_86400_sec_quincy_preemption_bounded_1024MB_flowlessly_relax/
./build/src/simulator --flagfile=/home/srguser/firmament-experiments/configs/google_40x_speedup_86400_sec_quincy_preemption_bounded_1024MB_flowlessly_relax.cfg
scp -r /mnt/data/google_40x_speedup_86400_sec_quincy_preemption_bounded_1024MB_flowlessly_relax/ icg27@ganymede.cl.cam.ac.uk:/mnt/data/icg27/firmament_simulations/
