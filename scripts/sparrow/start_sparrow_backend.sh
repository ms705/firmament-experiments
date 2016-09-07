#!/bin/bash

SPARROW_HOME="${HOME}/sparrow"

java -cp ${SPARROW_HOME}/target/sparrow-1.0-SNAPSHOT.jar \
  edu.berkeley.sparrow.examples.ShellCommandBackend
