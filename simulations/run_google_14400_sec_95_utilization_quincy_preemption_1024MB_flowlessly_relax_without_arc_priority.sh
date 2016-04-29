#!/bin/bash
cd ~/firmament/build/third_party/flowlessly/src/flowlessly/
git checkout master
# Relax without arc priority
git checkout 7f059ca9519e4e43b9a240268f6d3592cd03f1b3
cmake .
make clean; make -j3
cd ~/firmament
rm -r /mnt/data/google_14400_sec_95_utilization_quincy_preemption_bounded_1024MB_flowlessly_relax_without_arc_priority/
mkdir /mnt/data/google_14400_sec_95_utilization_quincy_preemption_bounded_1024MB_flowlessly_relax_without_arc_priority/
./build/src/simulator --flagfile=/home/srguser/firmament-experiments/configs/google_14400_sec_95_utilization_quincy_preemption_bounded_1024MB_flowlessly_relax_without_arc_priority.cfg
scp -r /mnt/data/google_14400_sec_95_utilization_quincy_preemption_bounded_1024MB_flowlessly_relax_without_arc_priority/ icg27@ganymede.cl.cam.ac.uk:/mnt/data/icg27/firmament_simulations/
