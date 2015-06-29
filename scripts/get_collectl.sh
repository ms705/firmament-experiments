#!/bin/bash

if [[ $# -lt 3 ]]; then
  echo "usage: get_collect.sh <date> <from> <to>"
  exit 1
fi

DATE=$1
FROM=$2
TO=$3
FILENAME="/var/log/collectl/$(hostname)-${DATE}*.raw.gz"

rm /tmp/collectl-${FROM}-${TO}-$(hostname)-20150323.tab
collectl -scdmn -p ${FILENAME} --from ${FROM}-${TO} -ozTm -P -f /tmp/collectl-${FROM}-${TO}

