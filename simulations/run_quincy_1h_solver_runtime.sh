#!/bin/bash
# Cycle cancelling
ssh srguser@caelum-301.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_google_runtime_0.004events_flowlessly_cycle_cancelling.sh'
# Successive shortest
ssh srguser@caelum-302.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_google_runtime_0.004events_flowlessly_successive_shortest.sh'
ssh srguser@caelum-303.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_google_runtime_0.01events_flowlessly_successive_shortest.sh'
ssh srguser@caelum-304.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_google_runtime_0.02events_flowlessly_successive_shortest.sh'
ssh srguser@caelum-305.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_google_runtime_0.04events_flowlessly_successive_shortest.sh'
ssh srguser@caelum-306.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_google_runtime_0.1events_flowlessly_successive_shortest.sh'
ssh srguser@caelum-307.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_google_runtime_0.2events_flowlessly_successive_shortest.sh'
# Cost scaling
ssh srguser@caelum-308.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_google_14400_sec_quincy_preemption_bounded_1024MB_0.004events_flowlessly_cost_scaling.sh'
ssh srguser@caelum-309.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_google_14400_sec_quincy_preemption_bounded_1024MB_0.01events_flowlessly_cost_scaling.sh'
ssh srguser@caelum-310.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_google_14400_sec_quincy_preemption_bounded_1024MB_0.02events_flowlessly_cost_scaling.sh'
ssh srguser@caelum-311.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_google_14400_sec_quincy_preemption_bounded_1024MB_0.04events_flowlessly_cost_scaling.sh'
ssh srguser@caelum-312.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_google_14400_sec_quincy_preemption_bounded_1024MB_0.1events_flowlessly_cost_scaling.sh'
ssh srguser@caelum-313.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_google_14400_sec_quincy_preemption_bounded_1024MB_0.2events_flowlessly_cost_scaling.sh'
ssh srguser@caelum-314.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_google_14400_sec_quincy_preemption_bounded_1024MB_0.4events_flowlessly_cost_scaling.sh'
ssh srguser@caelum-401.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_google_14400_sec_quincy_preemption_bounded_1024MB_0.6events_flowlessly_cost_scaling.sh'
ssh srguser@caelum-402.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_google_14400_sec_quincy_preemption_bounded_1024MB_0.8events_flowlessly_cost_scaling.sh'
ssh srguser@caelum-403.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_google_14400_sec_quincy_preemption_bounded_1024MB_flowlessly_cost_scaling.sh'
# Relax
ssh srguser@caelum-404.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_google_runtime_0.004events_flowlessly_relax.sh'
ssh srguser@caelum-405.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_google_runtime_0.01events_flowlessly_relax.sh'
ssh srguser@caelum-406.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_google_runtime_0.02events_flowlessly_relax.sh'
ssh srguser@caelum-407.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_google_runtime_0.04events_flowlessly_relax.sh'
ssh srguser@caelum-408.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_google_runtime_0.1events_flowlessly_relax.sh'
ssh srguser@caelum-409.cl.cam.ac.uk 'screen -d -m /home/srguser/firmament-experiments/simulations/run_google_runtime_0.2events_flowlessly_relax.sh'
