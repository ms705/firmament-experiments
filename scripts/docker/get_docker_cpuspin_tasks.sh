#!/bin/bash
parallel-ssh -i -h ~/caelum_tmp "docker ps -a" | grep "cpu_spin" | tr -s ' ' | cut -d' ' -f15 | cut -d'.' -f3 >> docker_cpuspin_tasks.csv
