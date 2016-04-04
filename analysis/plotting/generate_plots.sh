#!/bin/bash

ssh ganymede.cl.cam.ac.uk './mnt/data/icg27/firmament-experiments/analysis/plotting/generate_quincy_pinned_scheduling_runtimes.sh'

scp ganymede.cl.cam.ac.uk:/mnt/data/icg27/firmament-experiments/analysis/plotting/*.pdf ./
