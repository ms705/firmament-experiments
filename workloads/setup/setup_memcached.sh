#!/bin/bash

sudo apt-get -y update
sudo apt-get -y install memcached rcconf

sudo rcconf --off memcached
sudo service memcached stop
