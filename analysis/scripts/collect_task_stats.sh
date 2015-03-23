#!/bin/bash

if [[ $# -lt 3 ]]; then
  echo "usage: collect_task_stats.sh <task ID> <coordinator URL> <output file>"
  exit 1
fi

TASK_ID=$1
COORD_URL=$2
OUT_FILE=$3

mkdir -p ${OUT_DIR}

curl -L "${COORD_URL}/stats/?task=${TASK_ID}" > ${OUT_FILE}
