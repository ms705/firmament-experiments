#!/bin/bash
# $1 file to which to write the runtimes
parallel-ssh -i -h ~/caelum_tmp "cat /tmp/sparrow_backend_out | grep completed" | grep completed | cut -d' ' -f11 > $1
