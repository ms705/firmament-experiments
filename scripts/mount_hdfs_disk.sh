#!/bin/bash

# Format the disk
sudo mkfs -t ext4 /dev/sdb1

# Add the disk to fstab
LINE="UUID="
DISK_UUID=`sudo blkid /dev/sdb1 | cut -d' ' -f 2 | cut -d'"' -f 2`

sudo echo "${LINE}${DISK_UUID} /mnt/data/ ext4 errors=remount-ro 0 1" >> /etc/fstab
sudo mkdir /mnt/data
sudo mount -a

sudo mkdir -p /mnt/data/hadoop-hdfs/cache/hdfs/dfs/
sudo mkdir -p /mnt/data/hadoop-hdfs/cache/hdfs/mapred/
sudo chmod -R 777 /mnt/data/hadoop-hdfs/

# if [[ $1 == "master" ]]; then
#     # Format the namenode
#     sudo su
#     su hdfs
#     hadoop namenode -format
#     exit
#     exit
# fi
sudo chmod -R 777 /mnt/data/hadoop-hdfs/
