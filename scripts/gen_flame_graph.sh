#!/bin/bash
perf record --output=/mnt/data/perf.data --call-graph dwarf -i ./build/src/simulator --flagfile=/home/srguser/firmament-experiments/configs/synthetic_c1000k_octopus_cs2.cfg
cd /mnt/data/
perf script > c1000k_octopus_cs2.perf
/home/srguser/FlameGraph/stackcollapse-perf.pl c1000k_octopus_cs2.perf > c1000k_octopus_cs2.folded
/home/srguser/FlameGraph/flamegraph.pl c1000k_octopus_cs2.folded > c1000k_octopus_cs2.svg
