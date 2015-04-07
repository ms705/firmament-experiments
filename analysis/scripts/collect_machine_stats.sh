#!/bin/bash

if [[ $# -lt 4 ]]; then
  echo "usage: collect_machine_stats.sh <date> <from> <to> <outdir>"
  exit 1
fi

DATE=$1
FROM=$2
TO=$3
OUT_DIR=$4

CMD="/home/srguser/firmament-experiments/scripts/get_collectl.sh ${DATE} ${FROM} ${TO}"
parallel-ssh -P -t 0 -h ~/hosts.all ${CMD}
for r in 3 4; do
  for i in `seq -w 1 14`; do
    scp caelum-${r}${i}:/tmp/collectl-$(printf %q "${FROM}")-$(printf %q "${TO}")-'*'-${DATE}.tab ${OUT_DIR}
  done
done
${CMD}
cp /tmp/collectl-$(printf %s "${FROM}")-$(printf %s "${TO}")-$(hostname)-${DATE}.tab ${OUT_DIR}/ 

