#!/bin/bash

if [[ $# -lt 1 ]]; then
  echo "usage: stop_cluster.sh <host file>"
  exit 1
fi

parallel-ssh -t 0 -h $1 "killall coordinator"
#parallel-ssh -t 0 -h $1 "curl http://localhost:8080/shutdown"
