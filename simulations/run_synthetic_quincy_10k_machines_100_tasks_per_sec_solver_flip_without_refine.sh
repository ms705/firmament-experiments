#!/bin/bash
cd firmament
rm -r /mnt/data/synthetic_quincy_10k_machines_100_tasks_per_sec_solver_flip_without_refine/
mkdir /mnt/data/synthetic_quincy_10k_machines_100_tasks_per_sec_solver_flip_without_refine/
./build/src/simulator --flagfile=/home/srguser/firmament-experiments/configs/synthetic_quincy_10k_machines_100_tasks_per_sec_solver_flip_without_refine.cfg
scp -r /mnt/data/synthetic_quincy_10k_machines_100_tasks_per_sec_solver_flip_without_refine/ icg27@ganymede.cl.cam.ac.uk:/mnt/data/icg27/firmament_simulations/
