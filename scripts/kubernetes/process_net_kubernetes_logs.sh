#!/bin/bash
rm /tmp/k8s_created_times
rm /tmp/k8s_started_times
rm /tmp/k8s_finished_times
for i in {0..23} ; do kubectl describe pods task-runtime-events$i- > /tmp/tmp_pod_description ; grep "Creation Time:" /tmp/tmp_pod_description | cut -d$'\t' -f2 >> /tmp/k8s_created_times ; grep "Started:" /tmp/tmp_pod_description | cut -d$'\t' -f4 >> /tmp/k8s_started_times ; grep "Finished:" /tmp/tmp_pod_description | cut -d$'\t' -f4 >> /tmp/k8s_finished_times ; done
for i in {0..95} ; do kubectl describe pods sssp-tw-edges$i- > /tmp/tmp_pod_description ; grep "Creation Time:" /tmp/tmp_pod_description | cut -d$'\t' -f2 >> /tmp/k8s_created_times ; grep "Started:" /tmp/tmp_pod_description | cut -d$'\t' -f4 >> /tmp/k8s_started_times ; grep "Finished:" /tmp/tmp_pod_description | cut -d$'\t' -f4 >> /tmp/k8s_finished_times ; done
for i in {0..191} ; do kubectl describe pods pagerank-uk-edges$i- > /tmp/tmp_pod_description ; grep "Creation Time:" /tmp/tmp_pod_description | cut -d$'\t' -f2 >> /tmp/k8s_created_times ; grep "Started:" /tmp/tmp_pod_description | cut -d$'\t' -f4 >> /tmp/k8s_started_times ; grep "Finished:" /tmp/tmp_pod_description | cut -d$'\t' -f4 >> /tmp/k8s_finished_times ; done

paste -d "," /tmp/k8s_created_times /tmp/k8s_started_times > /tmp/k8s_created_started_times
paste -d ","  /tmp/k8s_created_started_times /tmp/k8s_finished_times > kubernetes_times.csv
