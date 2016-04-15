#!/bin/bash
cd ~/firmament/build/third_party/flowlessly/src/flowlessly/
git checkout master
# Solver flip with price refine.
git checkout d7fc6ef7ef055d8f084a54e5f619303cfad979d0
cmake .
make clean; make -j3
cd ~/firmament
rm -r /mnt/data/synthetic_quincy_10k_machines_100_tasks_per_sec_solver_flip/
mkdir /mnt/data/synthetic_quincy_10k_machines_100_tasks_per_sec_solver_flip/
./build/src/simulator --flagfile=/home/srguser/firmament-experiments/configs/synthetic_quincy_10k_machines_100_tasks_per_sec_solver_flip.cfg
scp -r /mnt/data/synthetic_quincy_10k_machines_100_tasks_per_sec_solver_flip/ icg27@ganymede.cl.cam.ac.uk:/mnt/data/icg27/firmament_simulations/
