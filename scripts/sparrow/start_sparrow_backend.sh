#!/bin/bash

SPARROW_HOME="${HOME}/sparrow"
export PATH=${PATH}:${HOME}/firmament-experiments/workloads/synthetic/hdfs:${HOME}/firmament-experiments/workloads/synthetic/cpu_spin

java -cp ${SPARROW_HOME}/target/sparrow-1.0-SNAPSHOT.jar \
  edu.berkeley.sparrow.examples.ShellCommandBackend 1> /tmp/sparrow_backend_out 2> /tmp/sparrow_backend_err &
