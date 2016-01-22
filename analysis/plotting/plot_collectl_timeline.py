import matplotlib
import matplotlib.pyplot as plt
import os, sys
from datetime import datetime
from utils import *

paper_mode = True

def translate_label(lbl):
  if lbl == "[CPU]Totl%":
    return "CPU"
  elif lbl == "[MEM]Anon":
    return "RAM"
  elif lbl == "[DSK]KbTot":
    return "Disk I/O"
  elif lbl == "[NET]RxKBTot":
    return "Network receive"
  elif lbl == "[NET]TxKBTot":
    return "Network send"

if len(sys.argv) < 2:
  print "usage: plot_collectl_timeline.py <collectl file> <title> " \
    "<output file> <normalize> <metric 1> ... <metric N>"
  sys.exit(1)

input_file = sys.argv[1]
title = sys.argv[2]
output_file = sys.argv[3]
do_percent = bool(sys.argv[4])
metrics = sys.argv[5:]

if do_percent:
  print "Normalizing output values to percentages!"

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
      elif 'CPU' in labels[i]:
        dataseries[labels[i]].append(float(fields[i]))
      elif labels[i] == '[MEM]Tot':
        total_memory = int(fields[i])
      elif do_percent and "MEM" in labels[i] and labels[i] != '[MEM]Tot':
        # XXX(malte): dodgy hack!
        dataseries[labels[i]].append(float(fields[i]) / total_memory * 100)
      elif do_percent and "DSK" in labels[i]:
        dataseries[labels[i]].append(float(fields[i]) / 250000 * 100)
      elif do_percent and "NET" in labels[i]:
        dataseries[labels[i]].append(float(fields[i]) / 1170000 * 100)
      else:
        dataseries[labels[i]].append(float(fields[i]))

mpl_times = matplotlib.dates.date2num(times)
rel_times = [x * 24*60 for x in mpl_times - mpl_times[0]]
print max(rel_times)

if paper_mode:
  plt.figure(figsize=(2.3, 1))
else:
  plt.figure(figsize=(6, 2))

if paper_mode:
  set_paper_rcs()
else:
  set_rcs()

for m in metrics:
  #print "%s: " % (m),
  #print dataseries[m]
  plt.plot(rel_times, dataseries[m], label=translate_label(m))

if not paper_mode:
  plt.title(title, fontsize=8)
if do_percent:
  plt.ylim(0, 100)
  plt.yticks(range(0, 101, 20), [str(x) for x in range(0, 101, 20)])
  plt.ylabel("Utilization [\%]")
#plt.xlim(min(rel_times), max(rel_times))
plt.xticks(np.arange(0, max(rel_times), 5),
           ["%.0f" % (x) for x in np.arange(0, max(rel_times), 5)])
#plt.xlim(4, 14)
plt.xlabel("Experiment time [min]")
plt.legend(ncol=2, frameon=False, columnspacing=0.5, handletextpad=0.1)

if paper_mode:
  plt.savefig(output_file + ".pdf", format="pdf", bbox_inches='tight',
              pad_inches=0.01)
plt.savefig(output_file + ".png", format="png", bbox_inches='tight',
            pad_inches=0.01)
