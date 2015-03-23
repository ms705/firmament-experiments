import matplotlib
import matplotlib.pyplot as plt
import os, sys
from utils import *

if len(sys.argv) < 2:
  print "usage: plot_normalized_runtime_barchart.py <collated dir> " \
        "<baseline name> <setup name> <workload 1> ... <workload N> "
  sys.exit(1)

input_dir = sys.argv[1]
baseline_name = sys.argv[2]
setup_name = sys.argv[3]
workloads = sys.argv[4:]

outname = setup_name

i = 0
baseline_runtimes = []
setup_runtimes = []
normed_runtimes = []
for wl in workloads:
  # baseline
  bl_maxtimes = []
  for l in open("%s/%s_%s.csv" % (input_dir, baseline_name, wl)).readlines():
    if l[0] == "#":
      continue
    fields = [x.strip() for x in l.split(",")]
    bl_maxtimes.append(float(fields[4]))
  bl_runtime = np.mean(bl_maxtimes)
  baseline_runtimes.append(bl_runtime)
  # setup
  maxtimes = []
  for l in open("%s/%s_%s.csv" % (input_dir, setup_name, wl)).readlines():
    if l[0] == "#":
      continue
    fields = [x.strip() for x in l.split(",")]
    maxtimes.append(float(fields[4]))
  setup_runtime = np.mean(maxtimes)
  print "%s: %f (%fx %f)" % (wl, setup_runtime, (setup_runtime / bl_runtime), bl_runtime)
  setup_runtimes.append(setup_runtime)
  normed_runtimes.append(setup_runtime / bl_runtime)
  
#########################################
# Normed runtimes

plt.figure()

plt.bar(np.arange(len(workloads)), normed_runtimes, width=0.8, align="center")

plt.axhline(1.0, lw=1.0, ls='-', color='k')

#plt.ylim(0, 16000)
plt.ylabel("Normalized makespan")

#plt.xlabel("Workload")
plt.xticks(np.arange(len(workloads)), workloads, ha='center')

plt.savefig("%s_normed_runtimes.pdf" % (outname), format="pdf")
plt.savefig("%s_normed_runtimes.png" % (outname), format="png")

#########################################
# Raw runtimes
plt.clf()

plt.bar(np.arange(len(workloads)), baseline_runtimes, width=0.4, align="center", label="Ideal")
plt.bar(np.arange(len(workloads)) + 0.4, setup_runtimes, width=0.4, align="center", label="Shared cluster", color='r')

#plt.ylim(0, 16000)
plt.ylabel("Makespan [sec]")
plt.legend()

#plt.xlabel("Workload")
plt.xticks(np.arange(len(workloads)) + 0.2, workloads, ha='center')

plt.savefig("%s_runtimes.pdf" % (outname), format="pdf")
plt.savefig("%s_runtimes.png" % (outname), format="png")


