#!/bin/bash

cd /home/srguser/
git clone https://github.com/kubernetes/kubernetes.git
cd kubernetes
git checkout -t -b release-1.3 remotes/origin/release-1.3
sudo apt-get install golang-1.6-go golang-1.6
export PATH=$PATH:/usr/lib/go-1.6/bin
make
sudo cp /home/srguser/kubernetes/_output/local/bin/linux/amd64/kubectl /usr/local/bin/kubectl
sudo chmod +x /usr/local/bin/kubectl

parallel-ssh -i -h ~/caelum sudo apt-get -y install bridge-utils

# Update  nodes="vcap@10.10.103.250 vcap@10.10.103.162 vcap@10.10.103.223"
# role="ai i i" and NUM_NODES=${NUM_NODES:-3} in cluster/ubuntu/config-default.sh

# cd ~/kubernetes/cluster/
# KUBERNETES_PROVIDER=ubuntu ./kube-up.sh
# cd ~/kubernetes/cluster/ubuntu/
# KUBERNETES_PROVIDER=ubuntu ./deployAddons.sh
