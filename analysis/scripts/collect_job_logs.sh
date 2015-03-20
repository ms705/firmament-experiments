#!/bin/bash

if [[ $# -lt 3 ]]; then
  echo "usage: collect_job_logs.sh <job id> <coordinator URL>"
  exit 1
fi

JOB_ID=$1
COORD_URL=$2
OUT_DIR=$3

mkdir -p ${OUT_DIR}

TASK_IDS=$(curl "${COORD_URL}/job/dtg/?id=${JOB_ID}" | python -m json.tool | grep \"uid\" | cut -d':' -f2)

for id in ${TASK_IDS}; do
  curl -L "${COORD_URL}/tasklog/?id=${id}&a=1" > ${OUT_DIR}/${id}-stdout.log
  curl -L "${COORD_URL}/tasklog/?id=${id}&a=2" > ${OUT_DIR}/${id}-stderr.log
done
