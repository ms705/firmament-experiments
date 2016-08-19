#!/bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

# Make the docker image and tag it as "firmament-experiments"
docker build -t firmament/experiments ${DIR}
docker push firmament/experiments
