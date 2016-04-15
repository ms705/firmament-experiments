#!/bin/bash
ssh srguser@caelum-301.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_google_2x_speedup_14400_sec_quincy_preemption_bounded_1024MB_flowlessly_incremental_cost_scaling_then_relax.sh'
ssh srguser@caelum-302.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_google_5x_speedup_14400_sec_quincy_preemption_bounded_1024MB_flowlessly_incremental_cost_scaling_then_relax.sh'
ssh srguser@caelum-303.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_google_10x_speedup_14400_sec_quincy_preemption_bounded_1024MB_flowlessly_incremental_cost_scaling_then_relax.sh'
ssh srguser@caelum-304.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_google_20x_speedup_14400_sec_quincy_preemption_bounded_1024MB_flowlessly_incremental_cost_scaling_then_relax.sh'
ssh srguser@caelum-305.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_google_2x_speedup_14400_sec_quincy_preemption_bounded_1024MB_flowlessly_relax.sh'
ssh srguser@caelum-306.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_google_5x_speedup_14400_sec_quincy_preemption_bounded_1024MB_flowlessly_relax.sh'
ssh srguser@caelum-307.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_google_10x_speedup_14400_sec_quincy_preemption_bounded_1024MB_flowlessly_relax.sh'
ssh srguser@caelum-308.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_google_20x_speedup_14400_sec_quincy_preemption_bounded_1024MB_flowlessly_relax.sh'
