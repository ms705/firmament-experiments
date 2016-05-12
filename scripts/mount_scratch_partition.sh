#!/bin/bash

sudo swapoff /dev/sda5
sudo sed -e '/swap/ s/^#*/#/' -i /etc/fstab

# Format the disk
sudo mkfs -t ext4 /dev/sda5

# Add the disk to fstab
LINE="UUID="
DISK_UUID=`sudo blkid /dev/sda5 | cut -d' ' -f 2 | cut -d'"' -f 2`

sudo echo "${LINE}${DISK_UUID} /mnt/scratch/ ext4 errors=remount-ro 0 1" >> /etc/fstab
sudo mkdir /mnt/scratch
sudo mount -a

sudo chown -R srguser.srguser /mnt/scratch
