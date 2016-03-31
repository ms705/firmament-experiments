#!/bin/bash
rm -r /mnt/data/google_14400_sec_quincy_bounded_1024MB_cs2/
mkdir /mnt/data/google_14400_sec_quincy_bounded_1024MB_cs2/
cd firmament
./build/src/simulator --flagfile=/home/srguser/firmament-experiments/configs/google_14400_sec_quincy_bounded_1024MB_cs2.cfg
scp -r /mnt/data/google_14400_sec_quincy_bounded_1024MB_cs2/ icg27@ganymede.cl.cam.ac.uk:/mnt/data/icg27/firmament_simulations/
