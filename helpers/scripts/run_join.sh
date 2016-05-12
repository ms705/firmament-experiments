#!/bin/bash

for j in $(seq $2); do
  for i in $1; do
    JOB_ID=$(python naiad_submit.py localhost 8080 /home/srguser/firmament-experiments/workloads/naiad/Examples/bin/Debug/Examples.exe "join" join${i}_run${j} ${i} | grep "JOB ID" | cut -d' ' -f4)
    echo "JOIN, ${i} splits, run ${j}: ${JOB_ID}"
    /home/srguser/firmament-experiments/helpers/scripts/wait_for_job_completion.sh ${JOB_ID} http://caelum-301:8080
    sleep 30
  done
done
