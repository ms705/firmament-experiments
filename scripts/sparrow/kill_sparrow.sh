#!/bin/bash

procID=$(ps -ef | grep sparrow | awk '{ print $2 }' | head -1)
kill -9 $procID
procID=$(ps -ef | grep sparrow | awk '{ print $2 }' | head -1)
kill -9 $procID
procID=$(ps -ef | grep sparrow | awk '{ print $2 }' | tail -1)
kill -9 $procID
procID=$(ps -ef | grep sparrow | awk '{ print $2 }' | tail -1)
kill -9 $procID
