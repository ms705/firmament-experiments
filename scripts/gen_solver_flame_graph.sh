#!/bin/bash
perf record --output=/mnt/data/perf.data --call-graph dwarf -i ./build/flow_scheduler --graph_has_node_types=true --algorithm=relax --print_assignments=true --algorithm_initial_solver_runs=fast_cost_scaling --algorithm_number_initial_runs=1 --daemon=false --incremental_graphs=/local/scratch/icg27/code/FlowlesslyPrivate/incremental.in
cd /mnt/data/
perf script > c1000k_octopus_cs2.perf
/home/srguser/FlameGraph/stackcollapse-perf.pl c1000k_octopus_cs2.perf > c1000k_octopus_cs2.folded
/home/srguser/FlameGraph/flamegraph.pl c1000k_octopus_cs2.folded > c1000k_octopus_cs2.svg
