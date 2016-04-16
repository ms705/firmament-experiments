#!/bin/bash
cd ~/firmament/build/third_party/flowlessly/src/flowlessly/
git checkout master
# Pre supply arc prioritization and task removal improvement
git checkout cf5f86400613de8bf143234efaad9ac2db3e2714
cmake .
make clean; make -j3
cd ~/firmament
rm -r /mnt/data/google_86400_sec_quincy_preemption_bounded_1024MB_flowlessly_incremental_cost_scaling_then_non-recovering_relax/
mkdir /mnt/data/google_86400_sec_quincy_preemption_bounded_1024MB_flowlessly_incremental_cost_scaling_then_non-recovering_relax/
./build/src/simulator --flagfile=/home/srguser/firmament-experiments/configs/google_86400_sec_quincy_preemption_bounded_1024MB_flowlessly_incremental_cost_scaling_then_non-recovering_relax.cfg
scp -r /mnt/data/google_86400_sec_quincy_preemption_bounded_1024MB_flowlessly_incremental_cost_scaling_then_non-recovering_relax/ icg27@ganymede.cl.cam.ac.uk:/mnt/data/icg27/firmament_simulations/
