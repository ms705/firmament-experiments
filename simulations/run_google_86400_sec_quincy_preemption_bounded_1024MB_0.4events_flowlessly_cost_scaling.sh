#!/bin/bash
cd firmament
mkdir /mnt/data/google_86400_sec_quincy_preemption_bounded_1024MB_0.4events_flowlessly_cost_scaling/
rm -r /mnt/data/google_86400_sec_quincy_preemption_bounded_1024MB_0.4events_flowlessly_cost_scaling/
./build/src/simulator --flagfile=/home/srguser/firmament-experiments/configs/google_86400_sec_quincy_preemption_bounded_1024MB_0.4events_flowlessly_cost_scaling.cfg
scp -r /mnt/data/google_86400_sec_quincy_preemption_bounded_1024MB_0.4events_flowlessly_cost_scaling/ icg27@ganymede.cl.cam.ac.uk:/mnt/data/icg27/firmament_simulations/
