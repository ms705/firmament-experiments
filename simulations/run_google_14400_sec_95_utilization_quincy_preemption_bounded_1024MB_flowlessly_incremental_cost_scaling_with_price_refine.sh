#!/bin/bash
cd ~/firmament/build/third_party/flowlessly/src/flowlessly/
git checkout master
# Price refine after every algo run
git checkout 85fced4722d392463b7623f7775e33f369d40f44
cmake .
make clean; make -j3
cd ~/firmament
rm -r /mnt/data/google_14400_sec_95_utilization_quincy_preemption_bounded_1024MB_flowlessly_incremental_cost_scaling_with_price_refine/
mkdir /mnt/data/google_14400_sec_95_utilization_quincy_preemption_bounded_1024MB_flowlessly_incremental_cost_scaling_with_price_refine/
./build/src/simulator --flagfile=/home/srguser/firmament-experiments/configs/google_14400_sec_95_utilization_quincy_preemption_bounded_1024MB_flowlessly_incremental_cost_scaling_with_price_refine.cfg
scp -r /mnt/data/google_14400_sec_95_utilization_quincy_preemption_bounded_1024MB_flowlessly_incremental_cost_scaling_with_price_refine/ icg27@ganymede.cl.cam.ac.uk:/mnt/data/icg27/firmament_simulations/
