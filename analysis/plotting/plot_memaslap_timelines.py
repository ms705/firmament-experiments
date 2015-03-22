import matplotlib
import matplotlib.pyplot as plt
import os, sys
from utils import *

if len(sys.argv) < 2:
  print "usage: plot_memaslap_timelines.py <log dir> <outfile>"
  sys.exit(1)

logdir = sys.argv[1]

i = 0
dataseries = []
for f in os.listdir(logdir):
  throughput_avg = {}
  latency_avg = {}
  latency_std = {}
  if not "stdout" in f:
    continue
  for l in open("%s/%s" % (logdir, f)).readlines():
    fields = l.split()
    if len(fields) < 1:
      continue
    if fields[0] == "Total":
      cat = "total"
    elif fields[0] == "Set":
      cat = "set"
    elif fields[0] == "Get":
      cat = "get"
    if fields[0] != "Period":
      continue
    append_or_create(throughput_avg, cat, int(fields[3]))
    append_or_create(latency_avg, cat, int(fields[8]))
    if int(fields[8]) > 1000:
      print f
    append_or_create(latency_std, cat, float(fields[9]))
  dataseries.append((throughput_avg, latency_avg, latency_std))

plt.figure()
for ds in dataseries:
  plt.plot(range(0, 30, 2), ds[2]['total'][0:30], marker='x')

plt.ylim(0, 16000)
plt.ylabel("Latency stdev [usec]")

plt.xlabel("Experiment time [sec]")

plt.savefig(sys.argv[2], format="pdf")
