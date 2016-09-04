#!/bin/bash
# $1 path to the kubernetes log file
grep "Creation Time:" $1 | cut -d$'\t' -f2 > /tmp/k8s_created_times
grep "Started:" $1 | cut -d$'\t' -f4 > /tmp/k8s_started_times
grep "Finished:" $1 | cut -d$'\t' -f4 > /tmp/k8s_finished_times
paste -d "," /tmp/k8s_created_times /tmp/k8s_started_times > /tmp/k8s_created_started_times
paste -d ","  /tmp/k8s_created_started_times /tmp/k8s_finished_times > kubernetes_times.csv
