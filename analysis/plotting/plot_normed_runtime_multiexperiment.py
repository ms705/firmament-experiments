import matplotlib
import matplotlib.pyplot as plt
import os, sys
from utils import *

paper_mode = True

def translate_workload(wl):
  if "scc" in wl:
    return "SCC"
  elif "tpch" in wl:
    return "TPC-H"
  elif "kitty" in wl:
    return "Img.~analysis"
  elif "join" in wl:
    return "Sym.~JOIN"
  elif "pagerank" in wl:
    return "PageRank"
  elif "netflix" in wl:
    return "NetFlix"
  elif "sssp" in wl:
    return "SSSP"

if len(sys.argv) < 2:
  print "usage: plot_normed_runtime_multiexperiment.py " \
        "<collated dir, collated dir2, ..., collated dir N> " \
        "<baseline name> <setup name> <workload 1> ... <workload N> "
  sys.exit(1)

input_dir = sys.argv[1]
baseline_name = sys.argv[2]
setup_names = sys.argv[3].split(",")
workloads = sys.argv[4:]

outname = "multi-experiment"

normed_runtimes_by_workload = {}
for s in setup_names:
  baseline_runtimes = []
  baseline_stdevs = []
  setup_runtimes = []
  setup_stdevs = []
  normed_runtimes = []
  for wl in workloads:
    # baseline
    bl_maxtimes = []
    for l in open("%s/%s_%s.csv" % (input_dir, baseline_name, wl)).readlines():
      if l[0] == "#":
        continue
      fields = [x.strip() for x in l.split(",")]
      median_rt = float(fields[1])
      min_rt = float(fields[3])
      max_rt = float(fields[4])
      # we use the max because the job runtime is dominated by the longest
      # straggler
      bl_maxtimes.append(max_rt)
      if min_rt < 10.0 or min_rt * 2 < median_rt or min_rt * 2 < np.median(bl_maxtimes):
        print "WARNING: low minimum runtime %f on baseline (%s) for %s" % (min_rt, baseline_name, wl)
      if max_rt > 1000.0 or max_rt / 2 > median_rt or max_rt / 2 > np.median(bl_maxtimes):
        print "WARNING: large maximum runtime %f on baseline (%s) for %s" % (max_rt, baseline_name, wl)
    bl_avg_runtime = np.mean(bl_maxtimes)
    bl_std_runtime = np.std(bl_maxtimes)
    baseline_runtimes.append(bl_avg_runtime)
    baseline_stdevs.append(bl_std_runtime)
    # setup
    maxtimes = []
    for l in open("%s/%s_%s.csv" % (input_dir, s, wl)).readlines():
      if l[0] == "#":
        continue
      fields = [x.strip() for x in l.split(",")]
      median_rt = float(fields[1])
      min_rt = float(fields[3])
      max_rt = float(fields[4])
      # we use the max because the job runtime is dominated by the longest
      # straggler
      maxtimes.append(float(max_rt))
      if min_rt < 10.0 or min_rt * 2 < median_rt or min_rt * 2 < np.median(maxtimes):
        print "WARNING: low minimum runtime %f on setup (%s) for %s" % (min_rt, s, wl)
      if max_rt > 1000.0 or max_rt / 2 > median_rt or max_rt / 2 > np.median(maxtimes):
        print "WARNING: large maximum runtime %f on setup (%s) for %s" % (min_rt, baseline_name, wl)
    setup_avg_runtime = np.mean(maxtimes)
    setup_std_runtime = np.std(maxtimes)
    #print "%s: %f (%fx %f)" % (wl, setup_avg_runtime, (setup_avg_runtime / bl_avg_runtime), bl_avg_runtime)
    setup_runtimes.append(setup_avg_runtime)
    setup_stdevs.append(setup_std_runtime)
    normed_runtimes.append(setup_avg_runtime / bl_avg_runtime)
    append_or_create(normed_runtimes_by_workload, wl,
                     (setup_avg_runtime / bl_avg_runtime))
  print "%s," % (s) + ",".join(["%f" % (x) for x in normed_runtimes])

print normed_runtimes_by_workload

avg_normed_runtimes = []
std_normed_runtimes = []
for wl in workloads:
  avg_normed_runtimes.append(np.mean(normed_runtimes_by_workload[wl]))
  std_normed_runtimes.append(np.std(normed_runtimes_by_workload[wl]))

#########################################
# Normed runtimes

if paper_mode:
  plt.figure(figsize=(3, 2))
else:
  plt.figure()

if paper_mode:
  set_paper_rcs()
else:
  set_rcs()

plt.bar(np.arange(len(workloads)), avg_normed_runtimes,
        yerr=std_normed_runtimes, ecolor='k', width=0.4, align="center")

plt.axhline(1.0, lw=1.0, ls='-', color='k')

plt.legend(frameon=False, loc="upper left")

plt.ylim(0, 3.5)
plt.yticks(np.arange(0, 3.6, 0.5), ["%.1f $\\times$" % (x) for x in np.arange(0, 3.6, 0.5)])
plt.ylabel("Normalized runtime")

#plt.xlabel("Workload")
plt.xticks(np.arange(len(workloads)),
           [translate_workload(x) for x in workloads], ha='right', rotation=30)

plt.savefig("%s_normed_runtimes.pdf" % (outname), format="pdf",
            bbox_inches='tight', pad_inches=0.01)
plt.savefig("%s_normed_runtimes.png" % (outname), format="png",
            bbox_inches='tight', pad_inches=0.01)
