#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
import numpy as np
import re
from datetime import datetime

def get_dist_str(v):
  return "μ: {: >15.5f}, σ: {: >15.5f}, 1%: {: >15.5f}, 50%: {: >15.5f}, 99%: {: >15.5f}".format(np.mean(v), np.std(v), np.percentile(v, 1), np.median(v), np.percentile(v, 99))

def parse_master_log(input_file):
  task_events = {}
  task_durations = {}
  task_waittimes = {}
  total_tasks = 0
  for line in open(input_file).readlines():
    match = re.match("I[0-9]+ ([0-9\:\.]+)[ ]* [0-9]+ .+\] Added framework ([A-Za-z\_\-0-9]+)", line)
    if match:
      event_time = datetime.strptime(match.group(1), "%H:%M:%S.%f")
      event_task = match.group(2)
      if not event_task in task_events:
        task_events[event_task] = {}
      task_events[event_task]['submit'] = event_time

    match = re.match("I[0-9]+ ([0-9\:\.]+)[ ]* [0-9]+ .+\] Status update ([A-Z_]+) .+ for task ([A-Za-z\_\-0-9]+) of framework ([A-Za-z\_\-0-9]+) .*", line)
    if match:
      if 'cpuspin' not in line:
        event_time = datetime.strptime(match.group(1), "%H:%M:%S.%f")
        event_task = match.group(4)
        event_type = match.group(2)
        if not event_task in task_events:
          task_events[event_task] = {}
        if event_type == "TASK_RUNNING":
          task_events[event_task]['start'] = event_time
          waittime = event_time - task_events[event_task]['submit']
          task_waittimes[event_task] = waittime.total_seconds()
        elif event_type == "TASK_FINISHED":
          task_events[event_task]['end'] = event_time
          runtime = (task_events[event_task]['end'] - task_events[event_task]['start']).total_seconds() 
          task_durations[event_task] = runtime
          total_tasks += 1
        else:
          print "unhandled event of type %s for task %s" % (event_type, event_task)

  print "Mesos: %d total tasks" % (total_tasks)
  return (task_durations, task_waittimes)
