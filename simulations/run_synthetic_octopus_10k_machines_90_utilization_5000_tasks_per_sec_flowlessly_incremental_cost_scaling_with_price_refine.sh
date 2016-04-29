#!/bin/bash
cd ~/firmament/build/third_party/flowlessly/src/flowlessly/
git checkout master
# Price refine after every algo run
git checkout 85fced4722d392463b7623f7775e33f369d40f44
cmake .
make clean; make -j3
cd ~/firmament
rm -r /mnt/data/synthetic_octopus_10k_machines_90_utilization_5000_tasks_per_sec_flowlessly_incremental_cost_scaling_with_price_refine/
mkdir /mnt/data/synthetic_octopus_10k_machines_90_utilization_5000_tasks_per_sec_flowlessly_incremental_cost_scaling_with_price_refine/
./build/src/simulator --flagfile=/home/srguser/firmament-experiments/configs/synthetic_octopus_10k_machines_90_utilization_5000_tasks_per_sec_flowlessly_incremental_cost_scaling_with_price_refine.cfg
scp -r /mnt/data/synthetic_octopus_10k_machines_90_utilization_5000_tasks_per_sec_flowlessly_incremental_cost_scaling_with_price_refine/ icg27@ganymede.cl.cam.ac.uk:/mnt/data/icg27/firmament_simulations/
