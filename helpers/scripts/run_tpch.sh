#!/bin/bash

for j in $(seq $2); do
  for i in $1; do
    #parallel-ssh -h /home/srguser/hosts.all -t 0 "sudo sh -c 'sync; echo 3 > /proc/sys/vm/drop_caches'"
    JOB_ID=$(python naiad_submit.py localhost 8080 /home/srguser/firmament-experiments/workloads/naiad/Examples/bin/Debug/Examples.exe "tpch" tpch${i}_run${j} ${i} | grep "JOB ID" | cut -d' ' -f4)
    echo "TPC-H, ${i} splits, run ${j}: ${JOB_ID}"
    /home/srguser/firmament-experiments/helpers/scripts/wait_for_job_completion.sh ${JOB_ID} http://caelum-301:8080
    sleep 30
  done
done
