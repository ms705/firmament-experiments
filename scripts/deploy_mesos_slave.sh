#!/bin/bash

# Setup
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv E56151BF
DISTRO=$(lsb_release -is | tr '[:upper:]' '[:lower:]')
CODENAME=$(lsb_release -cs)

# Add the repository
echo "deb http://repos.mesosphere.io/${DISTRO} ${CODENAME} main" | \
  sudo tee /etc/apt/sources.list.d/mesosphere.list
sudo apt-get -y update

sudo apt-get -y install mesos

sudo service zookeeper stop
sudo sh -c "echo manual > /etc/init/zookeeper.override"

echo "zk://caelum-301:2181/mesos" | sudo tee /etc/mesos/zk

sudo service mesos-master stop
sudo sh -c "echo manual > /etc/init/mesos-master.override"

sudo service mesos-slave restart
