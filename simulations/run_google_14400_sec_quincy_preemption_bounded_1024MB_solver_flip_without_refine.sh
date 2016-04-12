#!/bin/bash
cd ~/firmament/build/third_party/flowlessly/src/flowlessly/
git checkout master
# Solver flip without price refine.
git checkout c364d168adcafb8927961cc7cc791527fc6440dd
cmake .
make clean; make -j3
cd ~/firmament
rm -r /mnt/data/google_14400_sec_quincy_preemption_bounded_1024MB_/
mkdir /mnt/data/google_14400_sec_quincy_preemption_bounded_1024MB_solver_flip_without_refine/
./build/src/simulator --flagfile=/home/srguser/firmament-experiments/configs/google_14400_sec_quincy_preemption_bounded_1024MB_solver_flip_without_refine.cfg
scp -r /mnt/data/google_14400_sec_quincy_preemption_bounded_1024MB_solver_flip_without_refine/ icg27@ganymede.cl.cam.ac.uk:/mnt/data/icg27/firmament_simulations/
