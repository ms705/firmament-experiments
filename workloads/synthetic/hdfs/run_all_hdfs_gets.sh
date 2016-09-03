#!/bin/bash

/usr/bin/time -a --output=hdfs_baseline_time -f "%E" ./hdfs_get caelum10g-301.cl.cam.ac.uk 8020 /input/test_data/task_runtime_events.csv

for i in `seq 0 7` ; do /usr/bin/time -a --output=hdfs_baseline_time -f "%E" ./hdfs_get caelum10g-301.cl.cam.ac.uk 8020 /input/sssp_tw_edges_splits8/sssp_tw_edges${i}.in ; done

for i in `seq 0 15` ; do /usr/bin/time -a --output=hdfs_baseline_time -f "%E" ./hdfs_get caelum10g-301.cl.cam.ac.uk 8020 /input/pagerank_uk-2007-05_edges_splits16/pagerank_uk-2007-05_edges${i}.in ; done

#for i in `seq 0 13` ; do /usr/bin/time -a --output=hdfs_baseline_time -f "%E" ./hdfs_get caelum10g-301.cl.cam.ac.uk 8020 /input/lineitem_splits14/lineitem${i}.in ; done

#/usr/bin/time -a --output=hdfs_baseline_time -f "%E" ./hdfs_get caelum10g-301.cl.cam.ac.uk 8020 /input/test_data/task_runtime_events.csv
