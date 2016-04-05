#!/bin/bash
cd firmament
rm -r /mnt/data/google_14400_sec_quincy_bounded_1024MB_0.6events_flowlessly_cost_scaling/
mkdir /mnt/data/google_14400_sec_quincy_bounded_1024MB_0.6events_flowlessly_cost_scaling/
./build/src/simulator --flagfile=/home/srguser/firmament-experiments/configs/google_14400_sec_quincy_bounded_1024MB_0.6events_flowlessly_cost_scaling.cfg
scp -r /mnt/data/google_14400_sec_quincy_bounded_1024MB_0.6events_flowlessly_cost_scaling/ icg27@ganymede.cl.cam.ac.uk:/mnt/data/icg27/firmament_simulations/