import sys, os, errno
import pycurl
import json
import subprocess, shlex
import numpy as np
from pprint import pprint
from utils import *

def get_runtimes(td, ls):
  ls.append(to_seconds(get_runtime(td)))
  for c in td['spawned']:
    get_runtimes(c, ls)

def get_runtime(td):
  rt = int(td['finish_time']) - int(td['start_time'])
  if rt <= 0:
    print "WARNING: zero or negative runtime found for task %d: " \
            "%dus" % (int(td['uid']), rt)
  return rt

def to_seconds(time):
  return time / 1000000.0

# ------------------------------------

if len(sys.argv) < 2:
  print "usage: runtime_stats_for_job.py <json job descriptor file> [print header]"
  sys.exit(1)

if len(sys.argv) == 3:
  print_header = True
else:
  print_header = False

input_file = sys.argv[1]

with open(input_file) as fd:
  data = json.load(fd)

root_td = data['root_task']
runtimes = []
get_runtimes(root_td, runtimes)

if print_header:
  print "avg,median,stdev,min,max"
print "%f,%f,%f,%f,%f" % (np.mean(runtimes), np.median(runtimes), np.std(runtimes), np.min(runtimes), np.max(runtimes))
  
