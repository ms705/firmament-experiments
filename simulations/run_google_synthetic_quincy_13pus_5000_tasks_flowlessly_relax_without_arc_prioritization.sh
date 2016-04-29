#!/bin/bash
cd ~/firmament/build/third_party/flowlessly/src/flowlessly/
git checkout master
# Relax without arc priority
git checkout 7f059ca9519e4e43b9a240268f6d3592cd03f1b3
cmake .
make clean; make -j3
cd ~/firmament
rm -r /mnt/data/google_synthetic_quincy_13pus_5000_tasks_flowlessly_relax_without_arc_prioritization/
mkdir /mnt/data/google_synthetic_quincy_13pus_5000_tasks_flowlessly_relax_without_arc_prioritization/
./build/src/simulator --flagfile=/home/srguser/firmament-experiments/configs/google_synthetic_quincy_13pus_5000_tasks_flowlessly_relax_without_arc_prioritization.cfg
scp -r /mnt/data/google_synthetic_quincy_13pus_5000_tasks_flowlessly_relax_without_arc_prioritization/ icg27@ganymede.cl.cam.ac.uk:/mnt/data/icg27/firmament_simulations/
