#!/bin/bash

parallel-ssh -t 1000 -h ~/caelum -i 'cd firmament ; git checkout ./ ; git checkout master ; git pull ; cd build/ ; eval $(ssh-agent) ; ssh-add ~/.ssh/flowlessly-deploy_rsa ; make -j12 '
