#!/bin/bash

cd firmament-experiments
git pull
git submodule init

# can't do this because of Naiad :(
#git submodule foreach git pull
DIR=${PWD}
cd ${PWD}/helpers/napper
git pull
