#!/bin/bash

if [[ $# -lt 1 ]]; then
  echo "usage: process_batch_jobs.sh <input dir> <output dir>"
  exit 1
fi

SETUP=$(basename $1)
OUT_DIR=$2

for d in $(ls $1); do
  if [[ ${d} == "logs" ]]; then
    continue
  fi
  echo "# avg, median, stdev, min, max" >  ${OUT_DIR}/${SETUP}_${d}.csv
  for f in $(ls $1/${d}); do
    echo "${d}/${f}"
    for j in $(ls $1/${d}/${f}); do
      echo "${d}/${f}/${j}"
      python runtime_stats_for_job.py ${j} >> ${OUT_DIR}/${SETUP}_${d}.csv
    done
  done
done
