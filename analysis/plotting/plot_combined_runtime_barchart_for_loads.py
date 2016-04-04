import matplotlib
import matplotlib.pyplot as plt
import os, sys
from utils import *

if len(sys.argv) < 2:
  print "usage: plot_combined_runtime_barchart_for_loads.py <input csv> " \
        "<wl1 name> <wl1 label> ... <wl N name> <wl N label>"
  sys.exit(1)

workloads = []
labels = {}
input_csv = sys.argv[1]
for i in range(2, len(sys.argv), 2):
  wl_name = sys.argv[i]
  wl_label = sys.argv[i+1]
  workloads.append(wl_name)
  labels[wl_name] = wl_label
  print "%s -> %s" % (wl_name, wl_label)

outname = "combined.pdf"

dataseries = {}
setups = []
for l in open(input_csv).readlines():
  fields = [x.strip() for x in l.split(",")]
  setup_name = fields[0]
  setups.append(setup_name)
  i = 1
  for wl in workloads:
    append_or_create(dataseries, wl, float(fields[i]))
    i += 1

#########################################
# Plot

plt.figure()

colors = ['b', 'r', 'g', 'c', 'y', 'm']

width = 0.8 / len(workloads)
print width
i = 0
for wl in workloads:
  plt.bar(np.arange(len(setups)) + i*width, dataseries[wl], width=width,
          align="center", label=labels[wl], color=colors[i % len(colors)])
  i += 1

plt.axhline(1.0, lw=1.0, ls='-', color='k')

plt.ylabel("Normalized makespan")
plt.ylim(0, 3.0)

plt.xticks(np.arange(len(setups)) + width * len(setups) / 2, setups, ha='center')
plt.xlim(-0.5, len(setups))

plt.legend(ncol=2)

plt.savefig("%s.pdf" % (outname), format="pdf")
plt.savefig("%s.png" % (outname), format="png")
