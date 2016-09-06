import sys
import httplib, urllib, re, sys, random
import binascii
import gflags
import threading
import time
import shlex
import argparse
import random
import subprocess
import Queue
from datetime import datetime

FLAGS = gflags.FLAGS
gflags.DEFINE_string('cluster_manager', 'swarm',
                     'Cluster manager to use: swarm | kubernetes')


def build_swarm_job_cmd(name, cmd):
  docker_base_cmd = "docker service create --replicas 1 --restart-condition=none --name"
  docker_image = " firmament/libhdfs3"
  docker_base_hosts = r""" /bin/bash -c "echo '10.0.0.10 caelum10g-101' >> /etc/hosts ; echo '10.0.0.14 caelum10g-105' >> /etc/hosts ; echo '10.0.0.15 caelum10g-106' >> /etc/hosts ; echo '10.0.0.16 caelum10g-107' >> /etc/hosts ; echo '10.0.0.18 caelum10g-109' >> /etc/hosts ; echo '10.0.0.23 caelum10g-204' >> /etc/hosts ; echo '10.0.0.27 caelum10g-208' >> /etc/hosts ; echo '10.0.0.28 caelum10g-209' >> /etc/hosts ; echo '10.0.0.29 caelum10g-210' >> /etc/hosts ; echo '10.0.0.30 caelum10g-211' >> /etc/hosts ; echo '10.0.0.31 caelum10g-212' >> /etc/hosts ; echo '10.0.0.32 caelum10g-213' >> /etc/hosts ; echo '10.0.0.34 caelum10g-301' >> /etc/hosts ; echo '10.0.0.35 caelum10g-302' >> /etc/hosts ; echo '10.0.0.36 caelum10g-303' >> /etc/hosts ; echo '10.0.0.37 caelum10g-304' >> /etc/hosts ; echo '10.0.0.38 caelum10g-305' >> /etc/hosts ; echo '10.0.0.39 caelum10g-306' >> /etc/hosts ; echo '10.0.0.40 caelum10g-307' >> /etc/hosts ; echo '10.0.0.41 caelum10g-308' >> /etc/hosts ; echo '10.0.0.42 caelum10g-309' >> /etc/hosts ; echo '10.0.0.43 caelum10g-310' >> /etc/hosts ; echo '10.0.0.44 caelum10g-311' >> /etc/hosts ; echo '10.0.0.45 caelum10g-312' >> /etc/hosts ; echo '10.0.0.46 caelum10g-313' >> /etc/hosts ; echo '10.0.0.47 caelum10g-314' >> /etc/hosts ; echo '10.0.0.48 caelum10g-401' >> /etc/hosts ; echo '10.0.0.49 caelum10g-402' >> /etc/hosts ; echo '10.0.0.50 caelum10g-403' >> /etc/hosts ; echo '10.0.0.51 caelum10g-404' >> /etc/hosts ; echo '10.0.0.52 caelum10g-405' >> /etc/hosts ; echo '10.0.0.53 caelum10g-406' >> /etc/hosts ; echo '10.0.0.54 caelum10g-407' >> /etc/hosts ; echo '10.0.0.55 caelum10g-408' >> /etc/hosts ; echo '10.0.0.56 caelum10g-409' >> /etc/hosts ; echo '10.0.0.57 caelum10g-410' >> /etc/hosts ; echo '10.0.0.58 caelum10g-411' >> /etc/hosts ; echo '10.0.0.59 caelum10g-412' >> /etc/hosts ; echo '10.0.0.60 caelum10g-413' >> /etc/hosts ; echo '10.0.0.61 caelum10g-414' >> /etc/hosts ; """
  return docker_base_cmd + " " + name + docker_image + docker_base_hosts + cmd


# 3 NGINX with 4 AB each
# 3 PS with 4 workers

def run_helper(cmd):
    try:
      ret = subprocess.call(cmd, shell=True)
    except Exception as e:
      print "ERROR submitted job to Kubernetes: %s" % (e)
      return (False, "")
    return (True, "")


def main(argv):
  try:
    argv = FLAGS(argv)
  except gflags.FlagsError as e:
    print('%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS))

  events = Queue.PriorityQueue()

  spin_index = 0
  index = 0
  for i in range(0, 96000, 8000):
    for task_index in range(0, 2):
      if FLAGS.cluster_manager == 'kubernetes':
        events.put((i, "kubectl create -f /home/srguser/firmament-experiments/scripts/kubernetes/net_jobs/task_runtime_events%d.yaml" % (index)))
        events.put((i, "kubectl create -f /home/srguser/firmament-experiments/scripts/kubernetes/cpuspin_jobs/cpu_spin%d.yaml" % (spin_index)))
        events.put((i, "kubectl create -f /home/srguser/firmament-experiments/scripts/kubernetes/cpuspin_jobs/cpu_spin%d.yaml" % (spin_index + 1)))
      elif FLAGS.cluster_manager == 'swarm':
        events.put((i, build_swarm_job_cmd("task_runtime_events%d" % (index), r"""/hdfs_get caelum10g-301 8020 /input/test_data/task_runtime_events.csv" """)))
        events.put((i, build_swarm_job_cmd("cpu_spin%d" % (spin_index), r"""/cpu_spin 7" """)))
        events.put((i, build_swarm_job_cmd("cpu_spin%d" % (spin_index + 1), r"""/cpu_spin 7" """)))
      index = index + 1
      spin_index = spin_index + 2

  # About 3.7GB of input (8)
  index = 0
  for i in range(2000, 96000, 8000):
    for task_index in range(0, 8):
      if FLAGS.cluster_manager == 'kubernetes':
        events.put((i, "kubectl create -f /home/srguser/firmament-experiments/scripts/kubernetes/net_jobs/sssp_tw_edges%d.yaml" % (index)))
        events.put((i, "kubectl create -f /home/srguser/firmament-experiments/scripts/kubernetes/cpuspin_jobs/cpu_spin%d.yaml" % (spin_index)))
        events.put((i, "kubectl create -f /home/srguser/firmament-experiments/scripts/kubernetes/cpuspin_jobs/cpu_spin%d.yaml" % (spin_index + 1)))
      elif FLAGS.cluster_manager == 'swarm':
        events.put((i, build_swarm_job_cmd("sssp_tw_edges%d" % (index), r"""/hdfs_get caelum10g-301 8020 /input/sssp_tw_edges_splits8/sssp_tw_edges%d.in" """ % (task_index))))
        events.put((i, build_swarm_job_cmd("cpu_spin%d" % (spin_index), r"""/cpu_spin 7" """)))
        events.put((i, build_swarm_job_cmd("cpu_spin%d" % (spin_index + 1), r"""/cpu_spin 7" """)))
      index = index + 1
      spin_index = spin_index + 2

  # About 3.9GB of input (16). Each task takes about 6-8 seconds.
  index = 0
  for i in range(6000, 96000, 8000):
    for task_index in range(0, 16):
      if FLAGS.cluster_manager == 'kubernetes':
        events.put((i, "kubectl create -f /home/srguser/firmament-experiments/scripts/kubernetes/net_jobs/pagerank_uk_edges%d.yaml" % (index)))
        events.put((i, "kubectl create -f /home/srguser/firmament-experiments/scripts/kubernetes/cpuspin_jobs/cpu_spin%d.yaml" % (spin_index)))
        events.put((i, "kubectl create -f /home/srguser/firmament-experiments/scripts/kubernetes/cpuspin_jobs/cpu_spin%d.yaml" % (spin_index + 1)))
      elif FLAGS.cluster_manager == 'swarm':
        events.put((i, build_swarm_job_cmd("pagerank_uk_edges%d" % (index), r"""/hdfs_get caelum10g-301 8020 /input/pagerank_uk-2007-05_edges_splits16/pagerank_uk-2007-05_edges%d.in" """ % (task_index))))
        events.put((i, build_swarm_job_cmd("cpu_spin%d" % (spin_index), r"""/cpu_spin 7" """)))
        events.put((i, build_swarm_job_cmd("cpu_spin%d" % (spin_index + 1), r"""/cpu_spin 7" """)))
      index = index + 1
      spin_index = spin_index + 2

  # We don't submit lineitem tasks as well because we would end up
  # oversubscribing the network too much.
  # # About 1.4GB of input (14). Each task takes about 6-8 seconds.
  # index = 0
  # for i in range(8000, 96000, 8000):
  #   for task_index in range(0, 14):
  #     if FLAGS.cluster_manager == 'kubernetes':
  #       events.put((i, "kubectl create -f /home/srguser/firmament-experiments/scripts/kubernetes/net_jobs/lineitem%d.yaml" % (index)))
  #     elif FLAGS.cluster_manager == 'swarm':
  #       events.put((i, build_swarm_job_cmd("lineitem%d" % (index), r"""/hdfs_get caelum10g-301 8020 /input/lineitem_splits14/lineitem%d.in" """ % (task_index))))
  #       events.put((i, build_swarm_job_cmd("cpu_spin%d" % (spin_index), r"""/cpu_spin 7" """)))
  #       events.put((i, build_swarm_job_cmd("cpu_spin%d" % (spin_index + 1), r"""/cpu_spin 7" """)))
  #     index = index + 1
  #     spin_index = spin_index + 2


  start_time = datetime.now()
  threads = []
  while events.empty() is False:
    (run_at_time, job) = events.get()
    time_diff = datetime.now() - start_time
    time_now_ms = (time_diff.days * 24 * 60 * 60 + time_diff.seconds) * 1000 + time_diff.microseconds / 1000
    if run_at_time <= time_now_ms:
      print '... Running at: ', time_now_ms
      run_thread = threading.Thread(target=run_helper, args=(job,))
      run_thread.start()
      if run_thread.is_alive():
        print "... running (%s)" % (job)
        threads.append(run_thread)
      else:
        print "... ERROR"
    else:
      events.put((run_at_time, job))

  for thread in threads:
    if thread.is_alive():
      while thread.is_alive():
        print "Error: thread is still alive"
        time.sleep(1)
      thread.join()
    else:
      thread.join()


if __name__ == '__main__':
  main(sys.argv)
