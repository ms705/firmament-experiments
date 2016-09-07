#!/bin/bash

SPARROW_HOME="${HOME}/sparrow"

java -XX:+UseConcMarkSweepGC -cp ${SPARROW_HOME}/target/sparrow-1.0-SNAPSHOT.jar \
  edu.berkeley.sparrow.daemon.SparrowDaemon -c ${SPARROW_HOME}/sparrow.conf  1> /tmp/sparrow_daemon_out 2> /tmp/sparrow_daemon_err &
