#!/bin/bash
cd firmament
rm -r /mnt/data/synthetic_octopus_10k_machines_600_tasks_per_sec_flowlessly_incremental_cost_scaling/
mkdir /mnt/data/synthetic_octopus_10k_machines_600_tasks_per_sec_flowlessly_incremental_cost_scaling/
./build/src/simulator --flagfile=/home/srguser/firmament-experiments/configs/synthetic_octopus_10k_machines_600_tasks_per_sec_flowlessly_incremental_cost_scaling.cfg
scp -r /mnt/data/synthetic_octopus_10k_machines_600_tasks_per_sec_flowlessly_incremental_cost_scaling/ icg27@ganymede.cl.cam.ac.uk:/mnt/data/icg27/firmament_simulations/
