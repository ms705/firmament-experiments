#!/bin/bash

if [[ $1 == "master" ]]; then
    sudo /etc/init.d/hadoop-hdfs-namenode restart
    sudo /etc/init.d/hadoop-hdfs-datanode restart
    sudo su
    su hdfs
    hadoop fs -mkdir /mnt/data/hadoop-hdfs/cache/mapred/mapred/
    hadoop fs -chmod -R 777 /

    exit
    exit
    sudo /etc/init.d/hadoop-0.20-mapreduce-jobtracker restart
fi

sudo /etc/init.d/hadoop-hdfs-datanode restart
sudo /etc/init.d/hadoop-0.20-mapreduce-tasktracker restart
