#!/bin/bash

ssh ganymede.cl.cam.ac.uk 'cd /mnt/data/icg27/firmament-experiments/analysis/plotting/ ; python plot_scheduler_runtime_cdf.py --trace_path="/mnt/data/icg27/firmament_simulations/old_quincy_pinned/google_14400_sec_quincy_bounded_1024MB_flowlessly_cost_scaling/,/mnt/data/icg27/firmament_simulations/old_quincy_pinned/google_14400_sec_quincy_bounded_1024MB_flowlessly_incremental_cost_scaling/,/mnt/data/icg27/firmament_simulations/old_quincy_pinned/google_14400_sec_quincy_bounded_1024MB_flowlessly_relax/,/mnt/data/icg27/firmament_simulations/old_quincy_pinned/google_14400_sec_quincy_bounded_1024MB_flowlessly_incremental_cost_scaling_then_relax/" --trace_labels="cost scaling,incremental cost scaling,relax,incremental relax" --runtimes_after_timestamp=11078671198'

scp ganymede.cl.cam.ac.uk:/mnt/data/icg27/firmament-experiments/analysis/plotting/*.pdf ./
