#!/bin/bash
cd firmament
rm -r /mnt/data/google_86400_sec_13pus_quincy_preemption_bounded_1024MB_rapid_26percent_data_threshold/
mkdir /mnt/data/google_86400_sec_13pus_quincy_preemption_bounded_1024MB_rapid_26percent_data_threshold/
./build/src/simulator --flagfile=/home/srguser/firmament-experiments/configs/google_86400_sec_13pus_quincy_preemption_bounded_1024MB_rapid_26percent_data_threshold.cfg
scp -r /mnt/data/google_86400_sec_13pus_quincy_preemption_bounded_1024MB_rapid_26percent_data_threshold/ icg27@ganymede.cl.cam.ac.uk:/mnt/data/icg27/firmament_simulations/