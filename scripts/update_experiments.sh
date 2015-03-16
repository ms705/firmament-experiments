#!/bin/bash

cd firmament-experiments
git pull
git submodule init
git submodule update
git submodule foreach git pull
