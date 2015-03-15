#!/bin/bash
hadoop jar /usr/lib/hadoop-0.20-mapreduce/hadoop-examples.jar sort input33554432 sorted33554432
hadoop fs -rm -r -f /user/icg27/sorted33554432
hadoop jar /usr/lib/hadoop-0.20-mapreduce/hadoop-examples.jar sort input33554432 sorted33554432
hadoop fs -rm -r -f /user/icg27/sorted33554432
hadoop jar /usr/lib/hadoop-0.20-mapreduce/hadoop-examples.jar sort input33554432 sorted33554432
hadoop fs -rm -r -f /user/icg27/sorted33554432
