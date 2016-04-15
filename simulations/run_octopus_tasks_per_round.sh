#!/bin/bash
# Relax
ssh srguser@caelum-301.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_synthetic_octopus_10k_machines_10_tasks_per_sec_flowlessly_relax.sh'
ssh srguser@caelum-303.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_synthetic_octopus_10k_machines_50_tasks_per_sec_flowlessly_relax.sh'
ssh srguser@caelum-304.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_synthetic_octopus_10k_machines_100_tasks_per_sec_flowlessly_relax.sh'
ssh srguser@caelum-306.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_synthetic_octopus_10k_machines_200_tasks_per_sec_flowlessly_relax.sh'
ssh srguser@caelum-311.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_synthetic_octopus_10k_machines_400_tasks_per_sec_flowlessly_relax.sh'
ssh srguser@caelum-312.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_synthetic_octopus_10k_machines_600_tasks_per_sec_flowlessly_relax.sh'
ssh srguser@caelum-313.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_synthetic_octopus_10k_machines_800_tasks_per_sec_flowlessly_relax.sh'
ssh srguser@caelum-314.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_synthetic_octopus_10k_machines_1000_tasks_per_sec_flowlessly_relax.sh'
ssh srguser@caelum-401.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_synthetic_octopus_10k_machines_1200_tasks_per_sec_flowlessly_relax.sh'
ssh srguser@caelum-402.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_synthetic_octopus_10k_machines_1400_tasks_per_sec_flowlessly_relax.sh'

# Cost scaling
ssh srguser@caelum-403.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_synthetic_octopus_10k_machines_10_tasks_per_sec_flowlessly_cost_scaling.sh'
ssh srguser@caelum-405.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_synthetic_octopus_10k_machines_50_tasks_per_sec_flowlessly_cost_scaling.sh'
ssh srguser@caelum-406.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_synthetic_octopus_10k_machines_100_tasks_per_sec_flowlessly_cost_scaling.sh'
ssh srguser@caelum-407.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_synthetic_octopus_10k_machines_200_tasks_per_sec_flowlessly_cost_scaling.sh'
ssh srguser@caelum-408.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_synthetic_octopus_10k_machines_400_tasks_per_sec_flowlessly_cost_scaling.sh'
ssh srguser@caelum-409.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_synthetic_octopus_10k_machines_600_tasks_per_sec_flowlessly_cost_scaling.sh'
ssh srguser@caelum-412.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_synthetic_octopus_10k_machines_800_tasks_per_sec_flowlessly_cost_scaling.sh'
ssh srguser@caelum-413.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_synthetic_octopus_10k_machines_1000_tasks_per_sec_flowlessly_cost_scaling.sh'
ssh srguser@caelum-414.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_synthetic_octopus_10k_machines_1200_tasks_per_sec_flowlessly_cost_scaling.sh'
#ssh srguser@caelum-301.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_synthetic_octopus_10k_machines_1400_tasks_per_sec_flowlessly_cost_scaling.sh'
