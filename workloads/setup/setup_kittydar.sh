#!/bin/bash

sudo apt-get -y update
sudo apt-get -y install nodejs npm libcairo2-dev libjpeg8-dev libpango1.0-dev libgif-dev

cd workloads/kittydar/
npm install nomnom canvas colors charm hog-descriptor svm brain graceful-fs
