#!/bin/bash
cd ~/firmament/build/third_party/flowlessly/src/flowlessly/
git checkout master
# Solver flip with price refine.
git checkout ca4e6681ceb1bf155a44c9c209f5fc7cf72ee2a5
cmake .
make clean; make -j3
cd ~/firmament
rm -r /mnt/data/google_3600_sec_quincy_13pus_solver_flip/
mkdir /mnt/data/google_3600_sec_quincy_13pus_solver_flip/
./build/src/simulator --flagfile=/home/srguser/firmament-experiments/configs/google_3600_sec_quincy_13pus_solver_flip.cfg
scp -r /mnt/data/google_3600_sec_quincy_13pus_solver_flip/ icg27@ganymede.cl.cam.ac.uk:/mnt/data/icg27/firmament_simulations/
