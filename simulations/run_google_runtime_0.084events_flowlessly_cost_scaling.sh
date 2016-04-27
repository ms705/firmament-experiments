#!/bin/bash
cd firmament
rm -r /mnt/data/google_runtime_0.084events_flowlessly_cost_scaling/
mkdir /mnt/data/google_runtime_0.084events_flowlessly_cost_scaling/
./build/src/simulator --flagfile=/home/srguser/firmament-experiments/configs/google_runtime_0.084events_flowlessly_cost_scaling.cfg
scp -r /mnt/data/google_runtime_0.084events_flowlessly_cost_scaling/ icg27@ganymede.cl.cam.ac.uk:/mnt/data/icg27/firmament_simulations/
