# SPEC CPU2006 workload interference benchmarking
# analysis script

import re, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import pylab

def usage():
  print "parse-results.py <result directory> <specification file> " \
      "<num iterations> <num setups> [fix-scale]"

if len(sys.argv) < 4:
  usage()
  sys.exit()

result_dir = sys.argv[1]
spec_file = sys.argv[2]
num_iterations = int(sys.argv[3])
num_setups = int(sys.argv[4])
if len(sys.argv) >= 6:
  fix_scale = bool(sys.argv[5])
else:
  fix_scale = False

baselines = {}
runtimes = {}
prev_cacheparam = None
prev_bm_name = None
for line in open(spec_file).readlines():
  spec_matches = re.match('([0-9]+)\s+([a-zA-Z0-9]+)\s+([0-9\_]+)\s+([0-1 ]+)',
                          line)
  run_id = int(spec_matches.group(1))
  run_bm = spec_matches.group(2)
  run_cacheparam = str(spec_matches.group(4))
  if (spec_matches.group(3) == "_"):
    # baseline case, ignore cacheparam
    run_corecount = 1
  else:
    # other case, need to figure out which pair this belongs to
    run_corecount = int(spec_matches.group(3))
  print "ANALYZING %d %s %d %s" \
      % (run_id, run_bm, run_corecount, run_cacheparam)
  run_log = open("%s/CPU2006.%03d.log" % (result_dir, run_id))
  for log_line in run_log.readlines():
    log_match = re.match("\s+Reported: ([0-9]+) ([0-9]+) ([0-9\.]+)", log_line)
    if log_match and run_corecount == 1:
      #print "found baseline runtime %f" % (float(log_match.group(3)))
      baselines[run_bm] = float(log_match.group(3))
    elif log_match:
      #print "found runtime %f" % (float(log_match.group(3)))

      if prev_cacheparam == run_cacheparam:
        # second benchmark of pair

        # add nested dict entries as required
        if run_cacheparam not in runtimes:
          runtimes[run_cacheparam] = {}
        if prev_bm_name not in runtimes[run_cacheparam]:
          runtimes[run_cacheparam][prev_bm_name] = {}
        if run_bm not in runtimes[run_cacheparam]:
          runtimes[run_cacheparam][run_bm] = {}
        # record the runtimes
        runtimes[run_cacheparam][prev_bm_name][run_bm] = \
            float(log_match.group(3))
        runtimes[run_cacheparam][run_bm][prev_bm_name] = \
            prev_runtime
      else:
        # first benchmark of pair
        prev_cacheparam = run_cacheparam
        prev_bm_name = run_bm
        prev_runtime = float(log_match.group(3))
#  if len(runtimes[run_bm][run_cat][run_coreid]) < num_iterations:
#    print "WARNING: fewer than the expected %d runs in log file %s!" % \
#      (num_iterations, run_log)
  if run_corecount == 1:
    print "Baseline %s: %f" % (run_bm, baselines[run_bm])

#print runtimes

dataseries = []
all_benchmarks = ["gromacs", "namd", "povray", "hmmer", "gamess", "calculix", \
              "h264ref", "sjeng", "perlbench", "gobmk", "cactusADM", "tonto", \
              "zeusmp", "wrf", "bzip2", "astar", "xalancbmk", "leslie3d", \
              "bwaves", "sphinx3", "omnetpp", "mcf", "soplex", "GemsFDTD", \
              "gcc", "milc", "libquantum", "lbm"]

benchmarks = []
# find out which benchmarks we have data for
for bm in all_benchmarks:
  if bm in baselines:
    benchmarks.append(bm)

for cp in runtimes.keys():
  final_array = np.zeros([len(baselines), len(baselines)], dtype=float)
  i = 0
  j = 0
  for bm1 in reversed(benchmarks):
    for bm2 in benchmarks:
      baseline1 = baselines[bm1]
      baseline2 = baselines[bm2]
      print "recording %s/%s/%s" % (cp, bm1, bm2)
      norm1 = runtimes[cp][bm1][bm2] / baseline1
      norm2 = runtimes[cp][bm1][bm2] / baseline2
      print "value is %f/%f, setting at [%d,%d]" % (norm1, norm2, i, j)
      final_array[i][j] = norm2
#      final_array[j][i] = norm2
      j = j + 1
    i = i + 1
    j = 0
  dataseries.append(final_array)

# Plotting
fig = plt.figure(figsize=(12,12))
pylab.rc('font', size='10.0')

i = 0
for ds in dataseries:
  if fix_scale:
    plt.matshow(ds, vmax=1.5, vmin=0.8)
  else:
    plt.matshow(ds)

  # add some
  #plt.ylabel('')
  #plt.ylim(-0.5, int(sys.argv[4])-0.5)
  #plt.xlabel('Core ID')
  #plt.xlim(-0.5, int(sys.argv[4])-0.5)
  #test_name = re.search("(.+)\.csv", sys.argv[2])
  plt.suptitle(runtimes.keys()[i], y=0.1)

  cb = plt.colorbar(shrink=1.0, format='%.3e')
  cb.set_label('Normalized runtime')

  plt.xticks(np.arange(len(benchmarks)), benchmarks)
  for tick in pylab.gca().xaxis.iter_ticks():
    tick[0].label2On = True
    tick[0].label1On = False
    tick[0].label2.set_rotation('vertical')
  rev_bm = list(benchmarks)
  rev_bm.reverse()
  plt.yticks(np.arange(len(benchmarks)), rev_bm)
  plt.xlim(-0.5, len(baselines)-0.5)
  plt.ylim(-0.5, len(baselines)-0.5)

  #plt.show()
  if fix_scale:
    plt.savefig("plots/ap-new-%d-fs.pdf" % i, format="pdf", bbox_inches='tight')
    plt.savefig("plots/ap-new-%d-fs.png" % i, format="png", bbox_inches='tight')
  else:
    plt.savefig("plots/ap-new-%d.pdf" % i, format="pdf", bbox_inches='tight')
    plt.savefig("plots/ap-new-%d.png" % i, format="png", bbox_inches='tight')

  i = i + 1
