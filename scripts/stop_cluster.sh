#!/bin/bash

if [[ $# -lt 1 ]]; then
  echo "usage: stop_cluster.sh <host file>"
  exit 1
fi

echo "Killing coordinators..."
#parallel-ssh -t 0 -h $1 "killall coordinator"
parallel-nuke -t 0 -h $1 "coordinator"
#parallel-ssh -t 0 -h $1 "curl http://localhost:8080/shutdown"

echo "Cleaning up zombies..."
parallel-ssh -t 0 -h $1 "fuser 8080/tcp | cut -d':' -f1 | xargs kill"
