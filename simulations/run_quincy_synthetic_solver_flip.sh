#!/bin/bash
ssh srguser@caelum-304.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_synthetic_quincy_10k_machines_100_tasks_per_sec_solver_flip.sh'
ssh srguser@caelum-305.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_synthetic_quincy_10k_machines_100_tasks_per_sec_solver_flip_without_refine.sh'
