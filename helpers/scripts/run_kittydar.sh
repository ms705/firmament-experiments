#!/bin/bash

for j in $(seq $2); do
  for i in $1; do
    JOB_ID=$(python kittydar_submit.py localhost 8080 /home/srguser/firmament-experiments/workloads/kittydar/testing/test.js " --count=100" kittydar${i}_run${j}_100mot ${i} | grep "JOB ID" | cut -d' ' -f4)
    echo "Kittydar, ${i} splits, run ${j}: ${JOB_ID}"
    /home/srguser/firmament-experiments/helpers/scripts/wait_for_job_completion.sh ${JOB_ID} http://caelum-301:8080
  done
done
