#!/bin/bash
cd firmament
rm -r /mnt/data/google_86400_sec_13pus_octopus_rapid/
mkdir /mnt/data/google_86400_sec_13pus_octopus_rapid/
./build/src/simulator --flagfile=/home/srguser/firmament-experiments/configs/google_86400_sec_13pus_octopus_rapid.cfg
scp -r /mnt/data/google_86400_sec_13pus_octopus_rapid/ icg27@ganymede.cl.cam.ac.uk:/mnt/data/icg27/firmament_simulations/
