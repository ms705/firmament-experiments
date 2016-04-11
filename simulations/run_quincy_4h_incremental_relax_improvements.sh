#!/bin/bash
ssh srguser@caelum-301.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_google_14400_sec_quincy_preemption_bounded_1024MB_flowlessly_incremental_cost_scaling_then_arc_prioritization_relax.sh'
ssh srguser@caelum-302.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_google_14400_sec_quincy_preemption_bounded_1024MB_flowlessly_incremental_cost_scaling_then_improved_rem_node_relax.sh'
ssh srguser@caelum-303.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_google_14400_sec_quincy_preemption_bounded_1024MB_flowlessly_incremental_cost_scaling_then_non-recovering_relax.sh'
