#!/bin/bash

COMMON_EVENTS="cpu-clock task-clock context-switches cpu-migrations page-faults cycles instructions branches branch-misses cache-misses cache-references stalled-cycles-frontend stalled-cycles-backend node-loads node-load-misses"
INTEL_EVENTS="mem-loads mem-stores"
AMD_EVENTS="LLC-loads LLC-stores LLC-load-misses"

IS_INTEL=$(cat /proc/cpuinfo | grep Intel)
# XXX(malte): hack for SRG test cluster
IS_INTEL_GAINESTOWN=$(cat /proc/cpuinfo | grep E5520)
IS_AMD=$(cat /proc/cpuinfo | grep AMD)

if [[ ( ${IS_INTEL} == "" && ${IS_AMD} != "" ) || ( ${IS_INTEL} != "" && ${IS_INTEL_GAINESTOWN} != "" ) ]]; then
  EVENTS="${COMMON_EVENTS} ${AMD_EVENTS}"
elif [[ ${IS_INTEL} != "" && ${IS_AMD} == "" ]]; then
  EVENTS="${COMMON_EVENTS} ${INTEL_EVENTS}"
else
  echo "Unknown processor architecture: neither Intel nor AMD!"
  exit 1
fi
