#!/bin/bash

cd workloads/Naiad
git submodule update
git pull
git checkout v0.4.2
chmod +x build_mono.sh
./build_mono.sh
