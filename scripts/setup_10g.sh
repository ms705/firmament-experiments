#!/bin/bash

# get the 1G IP suffix
IP=$(ifconfig em1 | grep "inet addr" | cut -d'.' -f4 | cut -d' ' -f1)

# set up the 10G interface
sudo ifconfig p1p1 up
sudo ifconfig p1p1 10.0.0.${IP}/24

if [[ $(ifconfig p1p1 | grep UP) == "" ]]; then 
  exit 1;
fi;
