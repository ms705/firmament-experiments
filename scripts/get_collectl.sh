#!/bin/bash

if [[ $# -lt 4 ]]; then
  echo "usage: get_collect.sh <date> <from> <to> <outdir>"
  exit 1
fi

DATE=$1
FROM=$2
TO=$3
OUTDIR=$4
FILENAME="/var/log/collectl/$(hostname)-${DATE}-000000.raw.gz"

rm /tmp/collectl-${FROM}-${TO}-$(hostname)-20150323.tab
collectl -scdmn -p ${FILENAME} --from ${FROM}-${TO} -oTm -P -f /tmp/collectl-${FROM}-${TO} -oz

