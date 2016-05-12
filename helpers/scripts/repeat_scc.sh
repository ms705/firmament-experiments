#!/bin/bash
SCALE=$1
START_TIME=$2
RUN_TIME=$3
CUR_TIME=${START_TIME}

i=${SCALE}
j=0
until [[ ${CUR_TIME} -gt $(expr ${START_TIME} + ${RUN_TIME}) ]]; do
  JOB_ID=$(python naiad_submit.py localhost 8080 /home/srguser/firmament-experiments/workloads/naiad/Examples/bin/Debug/Examples.exe "dd-stronglyconnectedcomponents 2000000 4000000" scc${i}_run${j} ${i} | grep "JOB ID" | cut -d' ' -f4)
  echo "SCC, ${i} splits, run ${j}: ${JOB_ID}"
  /home/srguser/firmament-experiments/helpers/scripts/wait_for_job_completion.sh ${JOB_ID} http://caelum-301:8080
  CUR_TIME=$(date "+%s")
  j=$(expr ${j} + 1)
done
