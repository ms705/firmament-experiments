#!/bin/bash
ssh srguser@caelum-411.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_google_86400_sec_quincy_batch_0.5_sec_preemption_bounded_1024MB_flowlessly_cost_scaling.sh'
ssh srguser@caelum-412.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_google_86400_sec_quincy_batch_0.5_sec_preemption_bounded_1024MB_flowlessly_incremental_relax.sh'
ssh srguser@caelum-413.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_google_86400_sec_quincy_batch_0.5_sec_preemption_bounded_1024MB_solver_choice.sh'
ssh srguser@caelum-414.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_google_86400_sec_quincy_preemption_bounded_1024MB_solver_choice.sh'
