#!/bin/bash

sudo apt-get -y update
sudo apt-get -y install nginx rcconf

sudo rcconf --off nginx
sudo service nginx stop
