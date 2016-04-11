#!/bin/bash
cd ~/firmament/build/third_party/flowlessly/src/flowlessly/
git checkout master
# Arc prioritization.
git checkout 482b7b5182e9ab7cec70d2a60fa4876eac8b8b00
cmake .
make clean; make -j3
cd ~/firmament
rm -r /mnt/data/google_14400_sec_quincy_preemption_bounded_1024MB_flowlessly_incremental_cost_scaling_then_arc_prioritization_relax/
mkdir /mnt/data/google_14400_sec_quincy_preemption_bounded_1024MB_flowlessly_incremental_cost_scaling_then_arc_prioritization_relax/
./build/src/simulator --flagfile=/home/srguser/firmament-experiments/configs/google_14400_sec_quincy_preemption_bounded_1024MB_flowlessly_incremental_cost_scaling_then_arc_prioritization_relax.cfg
scp -r /mnt/data/google_14400_sec_quincy_preemption_bounded_1024MB_flowlessly_incremental_cost_scaling_then_arc_prioritization_relax/ icg27@ganymede.cl.cam.ac.uk:/mnt/data/icg27/firmament_simulations/
