import matplotlib
import matplotlib.pyplot as plt
import os, sys
from datetime import datetime
from utils import *

if len(sys.argv) < 2:
  print "usage: plot_collectl_timeline.py <collectl file> <title> <output file> <metric 1> ... <metric N>"
  sys.exit(1)

input_file = sys.argv[1]
title = sys.argv[2]
output_file = sys.argv[3]
metrics = sys.argv[4:]

i = 0
labels = []
dataseries = {}
times = []
for l in open(input_file).readlines():
  if l[0] == "#" and l[0:5] != "#Date":
    continue
  elif l[0:5] == "#Date":
    fields = l.split()
    for f in fields:
      dataseries[f] = []
      labels.append(f)
    print labels
  else:
    fields = l.split()
    total_memory = 0
    for i in range(len(fields)):
      if labels[i] == "Time":
        dt = datetime.strptime(fields[i], "%H:%M:%S")
        times.append(dt)
      elif '%' in labels[i]:
        dataseries[labels[i]].append(float(fields[i]))
      elif labels[i] == '[MEM]Tot':
        total_memory = int(fields[i])
      elif "MEM" in labels[i] and labels[i] != '[MEM]Tot':
        # XXX(malte): dodgy hack!
        dataseries[labels[i]].append(float(fields[i]) / total_memory * 100)
      elif "DSK" in labels[i]:
        dataseries[labels[i]].append(float(fields[i]) / 350000 * 100)
      elif "NET" in labels[i]:
        dataseries[labels[i]].append(float(fields[i]) / 1170000 * 100)

mpl_times = matplotlib.dates.date2num(times)

plt.figure(figsize=(6,2))

for m in metrics:
  print "%s: " % (m),
  print dataseries[m]
  plt.plot(mpl_times, dataseries[m], label=m)

plt.title(title, fontsize=8)
plt.ylim(0, 100)
plt.ylabel("Capacity [%]")
plt.xlabel("Experiment time [sec]")
plt.legend(ncol=2, fontsize=6, frameon=False)

plt.savefig(output_file, format="png", bbox_inches='tight')
