#!/bin/bash
cd ~/firmament/build/third_party/flowlessly/src/flowlessly/
git checkout master
# Solver flip without price refine.
git checkout 2b7602386c2c017f0e86a90c1a2f04e98610d37f
cmake .
make clean; make -j3
cd ~/firmament
rm -r /mnt/data/google_3600_sec_quincy_90_utilization_solver_flip_without_refine/
mkdir /mnt/data/google_3600_sec_quincy_90_utilization_solver_flip_without_refine/
./build/src/simulator --flagfile=/home/srguser/firmament-experiments/configs/google_3600_sec_quincy_90_utilization_solver_flip_without_refine.cfg
scp -r /mnt/data/google_3600_sec_quincy_90_utilization_solver_flip_without_refine/ icg27@ganymede.cl.cam.ac.uk:/mnt/data/icg27/firmament_simulations/
