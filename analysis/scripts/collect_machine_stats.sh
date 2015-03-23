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
parallel-ssh -P -h ~/hosts.all ${CMD}
parallel-ssh -h ~/hosts.all scp /tmp/collectl-${FROM}-${TO}-'*'-${DATE}.tab caelum-301:/${OUT_DIR}/
${CMD}
cp /tmp/collectl-${FROM}-${TO}-'*'-${DATE}.tab ${OUT_DIR}/ 

