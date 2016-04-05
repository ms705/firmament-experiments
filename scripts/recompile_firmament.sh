#!/bin/bash

eval $(ssh-agent)
ssh-add ~/.ssh/flowlessly-deploy_rsa
cd firmament
git checkout ./
git checkout master
git pull
rm -rf build/
cmake -Bbuild -H. -DENABLE_FLOWLESSLY=ON -DCMAKE_CXX_COMPILER=clang++-3.6
cd build/
make -j12
