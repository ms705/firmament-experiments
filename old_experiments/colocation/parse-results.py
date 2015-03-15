# SPEC CPU2006 workload interference benchmarking
# analysis script

import re, sys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def usage():
  print "parse-results.py <result directory> <specification file> " \
      "<num iterations> <normalize: True|False>"

if len(sys.argv) < 3:
  usage()

result_dir = sys.argv[1]
spec_file = sys.argv[2]
num_iterations = int(sys.argv[3])
normalize = bool(int(sys.argv[4]))

runtimes = {}
num_runs = {}
bm_names = []
for line in open(spec_file).readlines():
  spec_matches = re.match('([0-9]+)\s+([a-zA-Z0-9]+)\s+([0-9]+)\s+([0-1 ]+)', line)
  run_id = int(spec_matches.group(1))
  run_bm = spec_matches.group(2)
  if not run_bm in bm_names:
    bm_names.append(run_bm)
  if not run_bm in num_runs:
    num_runs[run_bm] = 1
    run_cat = 1
  else:
    run_cat = num_runs[run_bm] + 1
    num_runs[run_bm] = num_runs[run_bm] + 1
  run_corecount = int(spec_matches.group(3))
  run_cacheparam = str(spec_matches.group(4))
  print "ANALYZING %d %s %d %s" % (run_id, run_bm, run_corecount, run_cacheparam)
  run_log = open("%s/CPU2006.%03d.log" % (result_dir, run_id))
  if not run_cat in runtimes:
    runtimes[run_cat] = {}
  if not run_bm in runtimes[run_cat]:
    runtimes[run_cat][run_bm] = []
  for log_line in run_log.readlines():
    log_match = re.match("\s+Reported: ([0-9]+) ([0-9]+) ([0-9\.]+)", log_line)
    if log_match:
      runtimes[run_cat][run_bm].append(float(log_match.group(3)))
  if len(runtimes[run_cat][run_bm]) < num_iterations:
    print "WARNING: fewer than the expected %d runs in log file %s!" % \
      (num_iterations, run_log)

bars = {}
norm_bars = {}
ebars = {}
bm_base_rts = []
for cat, l in runtimes.items():
#  for bm, rts in l.items():
  for bm in bm_names:
    rts = l[bm]
    avg_rt = sum(rts) / float(len(rts))
    stdev_rt = np.std(rts)
    if not cat in bars:
      bars[cat] = []
      ebars[cat] = []
    bars[cat].append(avg_rt)
    ebars[cat].append(stdev_rt)
    if cat == 1:
      bm_base_rts.append(avg_rt)

#print bars

# Plotting
fig = plt.figure(figsize=(20,4))
cats = []

# normalized values
for cat, rts in bars.items():
  i = 0
  for rt in rts:
    if not cat in norm_bars:
      norm_bars[cat] = []
    norm_bars[cat].append(rt / bm_base_rts[i])
    i = i + 1
  cats.append(cat)

test = np.arange(28)
#print test
width = 0.025
i = 0
colors = ['r', 'g', 'b', 'y', 'm', 'c', '0.5', '0.1', '0.7']

print "CATs: %d" % (len(cats))
for cat in cats:
#  print norm_bars[cat]
  if normalize:
    print "normalized BARs: %d" % (len(norm_bars[cat]))
    plt.bar(test+width*i, norm_bars[cat], width, color=colors[i % len(colors)])
  else:
    print "BARs: %d" % (len(bars[cat]))
    plt.bar(test+width*i, bars[cat], width, color=colors[i % len(colors)],
            yerr=ebars[cat], ecolor=colors[i % len(colors)])
  i = i + 1

plt.xticks(test+width*(len(runtimes)/2.0), bm_names, rotation='vertical')

#plt.show()
plt.savefig("test.pdf", format="pdf", bbox_inches='tight')
