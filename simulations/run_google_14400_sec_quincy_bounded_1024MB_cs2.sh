#!/bin/bash
mkdir /mnt/data/google_14400_sec_quincy_bounded_1024MB_cs2/
cd firmament
./build/src/simulator --flagfile=/home/srguser/firmament-experiments/configs/google_14400_sec_quincy_bounded_1024MB_cs2.cfg
