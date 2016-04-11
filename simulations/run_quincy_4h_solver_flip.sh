#!/bin/bash
ssh srguser@caelum-304.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_google_14400_sec_quincy_preemption_bounded_1024MB_solver_flip.sh'
ssh srguser@caelum-305.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_google_14400_sec_quincy_preemption_bounded_1024MB_solver_flip_without_refine.sh'
