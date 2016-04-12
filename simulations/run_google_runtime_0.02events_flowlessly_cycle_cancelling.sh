#!/bin/bash
cd firmament
rm -r /mnt/data/google_runtime_0.02events_flowlessly_cycle_cancelling/
mkdir /mnt/data/google_runtime_0.02events_flowlessly_cycle_cancelling/
./build/src/simulator --flagfile=/home/srguser/firmament-experiments/configs/google_runtime_0.02events_flowlessly_cycle_cancelling.cfg
scp -r /mnt/data/google_runtime_0.02events_flowlessly_cycle_cancelling/ icg27@ganymede.cl.cam.ac.uk:/mnt/data/icg27/firmament_simulations/
