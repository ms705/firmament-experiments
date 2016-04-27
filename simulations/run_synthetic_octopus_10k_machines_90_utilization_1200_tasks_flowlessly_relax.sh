#!/bin/bash
cd firmament
rm -r /mnt/data/synthetic_octopus_10k_machines_90_utilization_1200_tasks_flowlessly_relax/
mkdir /mnt/data/synthetic_octopus_10k_machines_90_utilization_1200_tasks_flowlessly_relax/
./build/src/simulator --flagfile=/home/srguser/firmament-experiments/configs/synthetic_octopus_10k_machines_90_utilization_1200_tasks_flowlessly_relax.cfg
scp -r /mnt/data/synthetic_octopus_10k_machines_90_utilization_1200_tasks_flowlessly_relax/ icg27@ganymede.cl.cam.ac.uk:/mnt/data/icg27/firmament_simulations/
