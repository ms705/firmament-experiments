#!/bin/bash
cd ~/firmament/build/third_party/flowlessly/src/flowlessly/
# Solver flip without price refine.
git checkout fd75adabaf52ec44b071da30ef5bc5d657131999
cmake .
make -j3
cd ~/firmament
rm -r /mnt/data/google_14400_sec_quincy_preemption_bounded_1024MB_/
mkdir /mnt/data/google_14400_sec_quincy_preemption_bounded_1024MB_solver_flip_without_refine/
./build/src/simulator --flagfile=/home/srguser/firmament-experiments/configs/google_14400_sec_quincy_preemption_bounded_1024MB_solver_flip_without_refine.cfg
scp -r /mnt/data/google_14400_sec_quincy_preemption_bounded_1024MB_solver_flip_without_refine/ icg27@ganymede.cl.cam.ac.uk:/mnt/data/icg27/firmament_simulations/
