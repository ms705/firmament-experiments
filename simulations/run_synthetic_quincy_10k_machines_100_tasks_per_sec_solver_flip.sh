#!/bin/bash
cd firmament
rm -r /mnt/data/synthetic_quincy_10k_machines_100_tasks_per_sec_solver_flip/
mkdir /mnt/data/synthetic_quincy_10k_machines_100_tasks_per_sec_solver_flip/
./build/src/simulator --flagfile=/home/srguser/firmament-experiments/configs/synthetic_quincy_10k_machines_100_tasks_per_sec_solver_flip.cfg
scp -r /mnt/data/synthetic_quincy_10k_machines_100_tasks_per_sec_solver_flip/ icg27@ganymede.cl.cam.ac.uk:/mnt/data/icg27/firmament_simulations/
