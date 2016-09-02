#!/bin/bash
docker service rm $(docker service ls | cut -d' ' -f 3 | tail -n +2)
