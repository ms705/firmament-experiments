#!/bin/bash

git clone https://github.com/ms705/firmament.git firmament
cd firmament
export NONINTERACTIVE=1
make -j 12
