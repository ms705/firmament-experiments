#!/bin/bash

if [[ $# -lt 1 ]]; then
  echo "usage: run_mix.sh <load: 20, 50, 80, 90, 100> <runtime in sec>"
  exit 1
fi

LOAD=$1
RUN_TIME=$2

function clean_up {
  kill ${KITTYDAR_PID}
  kill ${PAGERANK_PID}
  kill ${TPCH_PID}
  kill ${NETFLIX_PID}
  kill ${SCC_PID}
  kill ${JOIN_PID}
  kill ${SSSP_PID}
}

trap clean_up SIGHUP SIGINT SIGTERM

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
  JOIN_COUNT=7
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
  JOIN_COUNT=7
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
  JOIN_COUNT=7
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
  JOIN_COUNT=7
elif [[ ${LOAD} -eq 100 ]]; then
  TPCH_COUNT=28
  NETFLIX_COUNT=28
  KITTYDAR_COUNT=30
  PAGERANK_COUNT=20
  SCC_COUNT=10
  SSSP_COUNT=30
  MEMCACHED_COUNT=45
  MEMASLAP_COUNT=45
  NGINX_COUNT=45
  AB_COUNT=45
  JOIN_COUNT=7
fi

# service jobs
MEMCACHED_JOB_ID=$(python memcached_submit.py localhost 8080 /usr/bin/memcached "" ${MEMCACHED_COUNT} | grep "JOB ID" | cut -d' ' -f4)
echo "memcached: ${MEMCACHED_JOB_ID}"
sleep 1

NGINX_JOB_ID=$(python nginx_submit.py localhost 8080 /usr/sbin/nginx "" ${NGINX_COUNT} | grep "JOB ID" | cut -d' ' -f4)
echo "nginx: ${NGINX_JOB_ID}"
sleep 1

# wait for everything to come up
sleep 10

MEMASLAP_JOB_ID=$(python memaslap_submit.py localhost 8080 /home/srguser/firmament-experiments/workloads/memaslap/libmemcached-1.0.18/clients/memaslap "-t 800s -T 8 -S2s" ${MEMASLAP_COUNT} | grep "JOB ID" | cut -d' ' -f4)
echo "memaslap: ${MEMASLAP_JOB_ID}"
sleep 1

AB_JOB_ID=$(python ab_submit.py localhost 8080 /usr/bin/ab "-n 1000000 -c 10" ${AB_COUNT} | grep "JOB ID" | cut -d' ' -f4)
echo "ab: ${AB_JOB_ID}"
sleep 1

sleep 10

START_TIME=$(date "+%s")
echo "Started at $(date), will submit jobs for ${RUN_TIME} seconds."
echo "########################################################"
echo "----------- $(date) ------------"

./repeat_sssp.sh ${SSSP_COUNT} ${START_TIME} ${RUN_TIME} &
SSSP_PID=$!
sleep 10

# batch jobs
./repeat_kittydar.sh ${KITTYDAR_COUNT} ${START_TIME} ${RUN_TIME} &
KITTYDAR_PID=$!
sleep 10

./repeat_tpch.sh ${TPCH_COUNT} ${START_TIME} ${RUN_TIME} &
TPCH_PID=$!
sleep 10

./repeat_netflix.sh ${NETFLIX_COUNT} ${START_TIME} ${RUN_TIME} &
NETFLIX_PID=$!
sleep 10

./repeat_pagerank.sh ${PAGERANK_COUNT} ${START_TIME} ${RUN_TIME} &
PAGERANK_PID=$!
sleep 10

./repeat_scc.sh ${SCC_COUNT} ${START_TIME} ${RUN_TIME} &
SCC_PID=$!
sleep 10

./repeat_join.sh ${JOIN_COUNT} ${START_TIME} ${RUN_TIME} &
JOIN_PID=$!
sleep 10

CUR_TIME=${START_TIME}
until [[ ${CUR_TIME} -gt $(expr ${START_TIME} + ${RUN_TIME}) ]]; do
  sleep 10
  CUR_TIME=$(date "+%s")
done

echo "----------- $(date) ------------"
echo "########################################################"
echo "Time's up, waiting for batch jobs to finish..."

wait ${KITTYDAR_PID}
wait ${TPCH_PID}
wait ${NETFLIX_PID}
wait ${PAGERANK_PID}
wait ${SCC_PID}
wait ${JOIN_PID}

echo "Killing service jobs..."
curl -s "http://caelum-301:8080/job/status/?id=${AB_JOB_ID}&a=kill"
curl -s "http://caelum-301:8080/job/status/?id=${MEMASLAP_JOB_ID}&a=kill"
curl -s "http://caelum-301:8080/job/status/?id=${NGINX_JOB_ID}&a=kill"
curl -s "http://caelum-301:8080/job/status/?id=${MEMCACHED_JOB_ID}&a=kill"
