#!/bin/bash
cd firmament
rm -r /mnt/data/google_runtime_0.036events_flowlessly_successive_shortest/
mkdir /mnt/data/google_runtime_0.036events_flowlessly_successive_shortest/
./build/src/simulator --flagfile=/home/srguser/firmament-experiments/configs/google_runtime_0.036events_flowlessly_successive_shortest.cfg
scp -r /mnt/data/google_runtime_0.036events_flowlessly_successive_shortest/ icg27@ganymede.cl.cam.ac.uk:/mnt/data/icg27/firmament_simulations/
