#!/bin/bash

cd firmament
git pull
export NONINTERACTIVE=1
make -j 12
