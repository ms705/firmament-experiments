#!/bin/bash
cd firmament
rm -r /mnt/data/synthetic_octopus_10k_machines_800_tasks_per_sec_flowlessly_incremental_relax/
mkdir /mnt/data/synthetic_octopus_10k_machines_800_tasks_per_sec_flowlessly_incremental_relax/
./build/src/simulator --flagfile=/home/srguser/firmament-experiments/configs/synthetic_octopus_10k_machines_800_tasks_per_sec_flowlessly_incremental_relax.cfg
scp -r /mnt/data/synthetic_octopus_10k_machines_800_tasks_per_sec_flowlessly_incremental_relax/ icg27@ganymede.cl.cam.ac.uk:/mnt/data/icg27/firmament_simulations/
