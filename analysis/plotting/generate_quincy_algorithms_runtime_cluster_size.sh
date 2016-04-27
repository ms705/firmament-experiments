#!/bin/bash

cd /mnt/data/icg27/firmament-experiments/analysis/plotting/
python plot_algorithms_runtime_cluster_size.py --setups="0.004,0.01,0.02,0.04,0.1,0.2,0.4,0.6,0.8,1.0" --runtimes_after_timestamp=600000000 --trace_paths=/mnt/data/icg27/firmament_simulations/quincy/google_runtime_0.004events_flowlessly_cycle_cancelling/,/mnt/data/icg27/firmament_simulations/quincy/google_runtime_0.004events_flowlessly_successive_shortest/,/mnt/data/icg27/firmament_simulations/quincy/google_runtime_0.01events_flowlessly_successive_shortest/,/mnt/data/icg27/firmament_simulations/quincy/google_runtime_0.02events_flowlessly_successive_shortest/,/mnt/data/icg27/firmament_simulations/quincy/google_runtime_0.04events_flowlessly_successive_shortest/,/mnt/data/icg27/firmament_simulations/quincy/google_runtime_0.1events_flowlessly_successive_shortest/,/mnt/data/icg27/firmament_simulations/quincy/google_runtime_0.2events_flowlessly_successive_shortest/,/mnt/data/icg27/firmament_simulations/quincy/google_runtime_0.004events_flowlessly_relax/,/mnt/data/icg27/firmament_simulations/quincy/google_runtime_0.01events_flowlessly_relax/,/mnt/data/icg27/firmament_simulations/quincy/google_runtime_0.02events_flowlessly_relax/,/mnt/data/icg27/firmament_simulations/quincy/google_runtime_0.04events_flowlessly_relax/,/mnt/data/icg27/firmament_simulations/quincy/google_runtime_0.1events_flowlessly_relax/,/mnt/data/icg27/firmament_simulations/quincy/google_runtime_0.2events_flowlessly_relax/,/mnt/data/icg27/firmament_simulations/quincy/google_runtime_0.4events_flowlessly_relax/,/mnt/data/icg27/firmament_simulations/quincy/google_runtime_0.6events_flowlessly_relax/,/mnt/data/icg27/firmament_simulations/quincy/google_runtime_0.8events_flowlessly_relax/,/mnt/data/icg27/firmament_simulations/quincy/google_runtime_1.0events_flowlessly_relax/,/mnt/data/icg27/firmament_simulations/quincy/google_86400_sec_quincy_preemption_bounded_1024MB_0.004events_flowlessly_cost_scaling/,/mnt/data/icg27/firmament_simulations/quincy/google_86400_sec_quincy_preemption_bounded_1024MB_0.01events_flowlessly_cost_scaling/,/mnt/data/icg27/firmament_simulations/quincy/google_86400_sec_quincy_preemption_bounded_1024MB_0.02events_flowlessly_cost_scaling/,/mnt/data/icg27/firmament_simulations/quincy/google_86400_sec_quincy_preemption_bounded_1024MB_0.04events_flowlessly_cost_scaling/,/mnt/data/icg27/firmament_simulations/quincy/google_86400_sec_quincy_preemption_bounded_1024MB_0.1events_flowlessly_cost_scaling/,/mnt/data/icg27/firmament_simulations/quincy/google_86400_sec_quincy_preemption_bounded_1024MB_0.2events_flowlessly_cost_scaling/,/mnt/data/icg27/firmament_simulations/quincy/google_86400_sec_quincy_preemption_bounded_1024MB_0.4events_flowlessly_cost_scaling/,/mnt/data/icg27/firmament_simulations/quincy/google_86400_sec_quincy_preemption_bounded_1024MB_0.6events_flowlessly_cost_scaling/,/mnt/data/icg27/firmament_simulations/quincy/google_86400_sec_quincy_preemption_bounded_1024MB_0.8events_flowlessly_cost_scaling/,/mnt/data/icg27/firmament_simulations/quincy/google_86400_sec_quincy_preemption_bounded_1024MB_flowlessly_cost_scaling/ --paper_mode
mv algorithms_scalability.pdf quincy_algorithms_cluster_scalability.pdf
