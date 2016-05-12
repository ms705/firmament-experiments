#!/bin/bash

if [[ $# -lt 1 ]]; then
  echo "usage: run_mix.sh <load: 20, 50, 80, 90, 100>"
  exit 1
fi

LOAD=$1

# clean up old outputs
hadoop fs -rm -r -f /output

if [[ ${LOAD} -eq 20 ]]; then
  TPCH_COUNT=5
  NETFLIX_COUNT=7
  KITTYDAR_COUNT=6
  PAGERANK_COUNT=6
  SCC_COUNT=5
  SSSP_COUNT=2
  MEMCACHED_COUNT=9
  MEMASLAP_COUNT=9
  NGINX_COUNT=9
  AB_COUNT=9
elif [[ ${LOAD} -eq 50 ]]; then
  TPCH_COUNT=14
  NETFLIX_COUNT=14
  KITTYDAR_COUNT=15
  PAGERANK_COUNT=15
  SCC_COUNT=15
  SSSP_COUNT=5
  MEMCACHED_COUNT=22
  MEMASLAP_COUNT=22
  NGINX_COUNT=23
  AB_COUNT=23
elif [[ ${LOAD} -eq 80 ]]; then
  TPCH_COUNT=22
  NETFLIX_COUNT=22
  KITTYDAR_COUNT=24
  PAGERANK_COUNT=24
  SCC_COUNT=25
  SSSP_COUNT=8
  MEMCACHED_COUNT=36
  MEMASLAP_COUNT=36
  NGINX_COUNT=36
  AB_COUNT=36
elif [[ ${LOAD} -eq 90 ]]; then
  TPCH_COUNT=25
  NETFLIX_COUNT=25
  KITTYDAR_COUNT=27
  PAGERANK_COUNT=27
  SCC_COUNT=27
  SSSP_COUNT=9
  MEMCACHED_COUNT=40
  MEMASLAP_COUNT=40
  NGINX_COUNT=41
  AB_COUNT=41
elif [[ ${LOAD} -eq 100 ]]; then
  TPCH_COUNT=28
  NETFLIX_COUNT=28
  KITTYDAR_COUNT=30
  PAGERANK_COUNT=30
  SCC_COUNT=30
  SSSP_COUNT=10
  MEMCACHED_COUNT=45
  MEMASLAP_COUNT=45
  NGINX_COUNT=45
  AB_COUNT=45
fi

# dispatch jobs
MEMCACHED_JOB_ID=$(python memcached_submit.py localhost 8080 /usr/bin/memcached "" ${MEMCACHED_COUNT} | grep "JOB ID" | cut -d' ' -f4)
echo "memcached: ${MEMCACHED_JOB_ID}"
sleep 1

NGINX_JOB_ID=$(python nginx_submit.py localhost 8080 /usr/sbin/nginx "" ${NGINX_COUNT} | grep "JOB ID" | cut -d' ' -f4)
echo "nginx: ${NGINX_JOB_ID}"
sleep 1

TPCH_JOB_ID=$(python naiad_submit.py localhost 8080 /home/srguser/firmament-experiments/workloads/naiad/Examples/bin/Debug/Examples.exe "tpch" tpch${TPCH_COUNT}_run0 ${TPCH_COUNT} | grep "JOB ID" | cut -d' ' -f4)
echo "TPC-H: ${TPCH_JOB_ID}"
sleep 1

NETFLIX_JOB_ID=$(python naiad_submit.py localhost 8080 /home/srguser/firmament-experiments/workloads/naiad/Examples/bin/Debug/Examples.exe "netflix 1970" netflix1970_${NETFLIX_COUNT}_run0 ${NETFLIX_COUNT} | grep "JOB ID" | cut -d' ' -f4)
echo "Netflix: ${NETFLIX_JOB_ID}"
sleep 1

KITTYDAR_JOB_ID=$(python kittydar_submit.py localhost 8080 /home/srguser/firmament-experiments/workloads/kittydar/testing/test.js "" kittydar${KITTYDAR_COUNT}_run0 ${KITTYDAR_COUNT} | grep "JOB ID" | cut -d' ' -f4)
echo "Kittydar: ${KITTYDAR_JOB_ID}"
sleep 1

PAGERANK_JOB_ID=$(python naiad_submit.py localhost 8080 /home/srguser/firmament-experiments/workloads/naiad/Examples/bin/Debug/Examples.exe "pagerank" pagerank${PAGERANK_COUNT}_run0 ${PAGERANK_COUNT} | grep "JOB ID" | cut -d' ' -f4)
echo "PageRank: ${PAGERANK_JOB_ID}"
sleep 1

SCC_JOB_ID=$(python naiad_submit.py localhost 8080 /home/srguser/firmament-experiments/workloads/naiad/Examples/bin/Debug/Examples.exe "dd-stronglyconnectedcomponents 20000000 40000000" scc${SCC_COUNT}_run0 ${SCC_COUNT} | grep "JOB ID" | cut -d' ' -f4)
echo "SCC: ${PAGERANK_JOB_ID}"
sleep 1

MEMASLAP_JOB_ID=$(python memaslap_submit.py localhost 8080 /home/srguser/firmament-experiments/workloads/memaslap/libmemcached-1.0.18/clients/memaslap "-t 600s -T 8 -S2s" ${MEMASLAP_COUNT} | grep "JOB ID" | cut -d' ' -f4)
echo "memaslap: ${MEMASLAP_JOB_ID}"
sleep 1

AB_JOB_ID=$(python ab_submit.py localhost 8080 /usr/bin/ab "-n 1000000" ${AB_COUNT} | grep "JOB ID" | cut -d' ' -f4)
echo "ab: ${AB_JOB_ID}"
sleep 1


