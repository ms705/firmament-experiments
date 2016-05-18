#!/bin/bash

parallel-ssh -t 1000 -h ~/caelum -i 'cd firmament ; git checkout ./ ; git checkout master ; git pull ; rm -rf build/ ; cmake -Bbuild -H. -DENABLE_FLOWLESSLY=ON -DCMAKE_CXX_COMPILER=g++ '
