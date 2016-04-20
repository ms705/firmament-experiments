#!/bin/bash
rm -r /mnt/data/google_86400_sec_quincy_preemption_bounded_1024MB_solver_choice/
mkdir /mnt/data/google_86400_sec_quincy_preemption_bounded_1024MB_solver_choice/
cd firmament
./build/src/simulator --flagfile=/home/srguser/firmament-experiments/configs/google_86400_sec_quincy_preemption_bounded_1024MB_solver_choice.cfg
scp -r /mnt/data/google_86400_sec_quincy_preemption_bounded_1024MB_solver_choice/ icg27@ganymede.cl.cam.ac.uk:/mnt/data/icg27/firmament_simulations/
