#!/bin/bash
rm -rf /mnt/scratch/*
rm -rf ~/firmament-logs/
rm -rf ~/firmament-perf/
rm -rf /mnt/data/firmament-coordlogs/coordinator.*
parallel-ssh -h ~/hosts.all -t 0 "sudo rm -rf /mnt/scratch/*"
parallel-ssh -h ~/hosts.all -t 0 "sudo rm -rf firmament-logs"
parallel-ssh -h ~/hosts.all -t 0 "sudo rm -rf firmament-perf"
parallel-ssh -h ~/hosts.all -t 0 "sudo rm -rf /tmp/coordinator.*"
