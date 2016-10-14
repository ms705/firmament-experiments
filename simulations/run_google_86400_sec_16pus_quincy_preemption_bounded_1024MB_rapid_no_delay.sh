#!/bin/bash
cd firmament
rm -r /mnt/data/google_86400_sec_16pus_quincy_preemption_bounded_1024MB_rapid_no_delay/
mkdir /mnt/data/google_86400_sec_16pus_quincy_preemption_bounded_1024MB_rapid_no_delay/
./build/src/simulator --flagfile=/home/srguser/firmament-experiments/configs/google_86400_sec_16pus_quincy_preemption_bounded_1024MB_rapid_no_delay.cfg
scp -r /mnt/data/google_86400_sec_16pus_quincy_preemption_bounded_1024MB_rapid_no_delay/ icg27@ganymede.cl.cam.ac.uk:/mnt/data/icg27/firmament_simulations/
