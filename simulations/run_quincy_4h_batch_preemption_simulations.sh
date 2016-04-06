#!/bin/bash
ssh srguser@caelum-301.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_google_14400_sec_quincy_batch_1_sec_preemption_bounded_1024MB_flowlessly_incremental_relax.sh'
ssh srguser@caelum-302.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_google_14400_sec_quincy_batch_2_sec_preemption_bounded_1024MB_flowlessly_incremental_relax.sh'
ssh srguser@caelum-303.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_google_14400_sec_quincy_batch_5_sec_preemption_bounded_1024MB_flowlessly_incremental_relax.sh'
ssh srguser@caelum-304.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_google_14400_sec_quincy_batch_10_sec_preemption_bounded_1024MB_flowlessly_incremental_relax.sh'
