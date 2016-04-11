#!/bin/bash
cd ~/firmament/build/third_party/flowlessly/src/flowlessly/
# Solver flip with price refine.
git checkout a985b929370101623d8c3929e1802e90d593878f
cmake .
make -j3
cd ~/firmament
rm -r /mnt/data/google_14400_sec_quincy_preemption_bounded_1024MB_/
mkdir /mnt/data/google_14400_sec_quincy_preemption_bounded_1024MB_solver_flip/
./build/src/simulator --flagfile=/home/srguser/firmament-experiments/configs/google_14400_sec_quincy_preemption_bounded_1024MB_solver_flip.cfg
scp -r /mnt/data/google_14400_sec_quincy_preemption_bounded_1024MB_solver_flip/ icg27@ganymede.cl.cam.ac.uk:/mnt/data/icg27/firmament_simulations/
