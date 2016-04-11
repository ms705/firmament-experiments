#!/bin/bash
cd ~/firmament/build/third_party/flowlessly/src/flowlessly/
git checkout master
# Task removal improvement
git checkout a0c07c247574c3bd74ba85747aa2c915580a92e3
cmake .
make clean; make -j3
cd ~/firmament
rm -r /mnt/data/google_14400_sec_quincy_preemption_bounded_1024MB_flowlessly_incremental_cost_scaling_then_improved_rem_node_relax/
mkdir /mnt/data/google_14400_sec_quincy_preemption_bounded_1024MB_flowlessly_incremental_cost_scaling_then_improved_rem_node_relax/
./build/src/simulator --flagfile=/home/srguser/firmament-experiments/configs/google_14400_sec_quincy_preemption_bounded_1024MB_flowlessly_incremental_cost_scaling_then_improved_rem_node_relax.cfg
scp -r /mnt/data/google_14400_sec_quincy_preemption_bounded_1024MB_flowlessly_incremental_cost_scaling_then_improved_rem_node_relax/ icg27@ganymede.cl.cam.ac.uk:/mnt/data/icg27/firmament_simulations/
