#!/bin/bash

for y in 1980; do
  for j in $(seq $2); do
    for i in $1; do
      JOB_ID=$(python naiad_submit.py localhost 8080 /home/srguser/firmament-experiments/workloads/naiad/Examples/bin/Debug/Examples.exe "netflix ${y}" netflix${y}_${i}_run${j} ${i} | grep "JOB ID" | cut -d' ' -f4)
      echo "NETFLIX/${y}, ${i} splits, run ${j}: ${JOB_ID}"
      /home/srguser/firmament-experiments/helpers/scripts/wait_for_job_completion.sh ${JOB_ID} http://caelum-301:8080
      sleep 30
    done
  done
done
