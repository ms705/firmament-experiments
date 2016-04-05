#!/bin/bash

# required for perf support
sudo apt-get -y install linux-tools-common
sudo apt-get -y install linux-tools-`uname -r`

# required for napper
sudo apt-get -y install python-kazoo python-netifaces

# actual Firmament
git clone https://github.com/ms705/firmament.git firmament
eval $(ssh-agent)
ssh-add ~/.ssh/flowlessly-deploy_rsa
cd firmament
cmake -Bbuild -H. -DENABLE_FLOWLESSLY=ON -DCMAKE_CXX_COMPILER=clang++-3.6
cd build/
make -j12
