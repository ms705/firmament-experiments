#!/bin/bash

# required for perf support
sudo apt-get -y install linux-tools-common
sudo apt-get -y install linux-tools-`uname -r`

# required for napper
sudo apt-get -y install python-kazoo

# actual Firmament
git clone https://github.com/ms705/firmament.git firmament
cd firmament
export NONINTERACTIVE=1
make -j 12
