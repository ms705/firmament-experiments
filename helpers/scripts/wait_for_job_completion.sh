#!/bin/bash

if [[ $# -lt 2 ]]; then
  echo "usage: wait_for_job_completion.sh <job ID> <coordinator URL>"
  exit 1
fi

JOB_ID=$1
COORD_URL=$2

STATUS=$(curl -s -L "${COORD_URL}/job/completion/?id=${JOB_ID}&json=1")

while [[ ${STATUS} != "COMPLETED" && ${STATUS} != "FAILED" && ${STATUS} != "ABORTED" ]]; do
  #echo "Still running..."
  sleep 10
  STATUS=$(curl -s -L "${COORD_URL}/job/completion/?id=${JOB_ID}&json=1")
done

echo "Done at $(date)!"
