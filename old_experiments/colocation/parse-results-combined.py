# SPEC CPU2006 workload interference benchmarking
# analysis script

import re, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def usage():
  print "parse-results.py <result directory> <specification file> " \
      "<num iterations> <num setups>"

if len(sys.argv) < 4:
  usage()
  sys.exit()

result_dir = sys.argv[1]
spec_file = sys.argv[2]
num_iterations = int(sys.argv[3])
num_setups = int(sys.argv[4])

runtimes = {}
num_runs = {}
bm_names = []
current_experiment = 0
exp_idx = {}
for line in open(spec_file).readlines():
  spec_matches = re.match('([0-9]+)\s+([a-zA-Z0-9]+)\s+([0-9]+)\s+([0-1 ]+)',
                          line)
  run_id = int(spec_matches.group(1))
  run_bm = spec_matches.group(2)
  run_corecount = int(spec_matches.group(3))
  run_cacheparam = str(spec_matches.group(4))
  if not run_bm in bm_names:
    bm_names.append(run_bm)
  if not run_bm in exp_idx:
    exp_idx[run_bm] = { run_corecount : { run_cacheparam : current_experiment } }
    run_exp = current_experiment
    current_experiment = current_experiment + 1
  elif not run_corecount in exp_idx[run_bm]:
    exp_idx[run_bm][run_corecount] = { run_cacheparam : current_experiment }
    run_exp = current_experiment
    current_experiment = current_experiment + 1
  elif not run_cacheparam in exp_idx[run_bm][run_corecount]:
    exp_idx[run_bm][run_corecount][run_cacheparam] = current_experiment
    run_exp = current_experiment
    current_experiment = current_experiment + 1
  else:
    run_exp = exp_idx[run_bm][run_corecount][run_cacheparam]
  run_cat = run_exp % num_setups
  if not run_bm in runtimes:
    runtimes[run_bm] = {}
  if not run_cat in runtimes[run_bm]:
    runtimes[run_bm][run_cat] = {}
  run_coreid = len(runtimes[run_bm][run_cat])
  if not run_coreid in runtimes[run_bm][run_cat]:
    runtimes[run_bm][run_cat][run_coreid] = []
  print "ANALYZING %d %s %d %s, CAT %d, EXP %d, CORE %d" \
      % (run_id, run_bm, run_corecount, run_cacheparam, run_cat, run_exp,
         run_coreid)
  run_log = open("%s/CPU2006.%03d.log" % (result_dir, run_id))
  for log_line in run_log.readlines():
    log_match = re.match("\s+Reported: ([0-9]+) ([0-9]+) ([0-9\.]+)", log_line)
    if log_match:
      runtimes[run_bm][run_cat][run_coreid].append(float(log_match.group(3)))
  if len(runtimes[run_bm][run_cat][run_coreid]) < num_iterations:
    print "WARNING: fewer than the expected %d runs in log file %s!" % \
      (num_iterations, run_log)

# Post-processing into data series
base_avg_rts = []
cats = []
bars = {}
ebars = {}
#for bm, cat_list in sorted(runtimes.items()):
for bm in bm_names:
  cat_list = runtimes[bm]
  print "Post-processing data for %s" % (bm)
  per_core_avg_rts = {}
  for cat, core_list in cat_list.items():
    if not cat in per_core_avg_rts:
      per_core_avg_rts[cat] = []
    for core_id, rts in core_list.items():
      avg_rt = np.mean(rts)
      per_core_avg_rts[cat].append(avg_rt)
      if cat == 0:
        if core_id == 0:
          # use this as a basis for normalization
          base_avg_rts.append(avg_rt)
        else:
          # this should never occur
          print "CAT: %d, CORE: %d" % (cat, core_id)
          assert(False)
  # iterate again, and normalize
  for cat, avg_rts in per_core_avg_rts.items():
    norm_rts = []
    for rt in avg_rts:
      norm_rt = rt / per_core_avg_rts[0][0]
      norm_rts.append(norm_rt)
    if len(norm_rts) > 1:
      avg_normed_avgs = np.mean(norm_rts)
      dev_normed_avgs = (avg_normed_avgs - min(norm_rts),
                         max(norm_rts) - avg_normed_avgs)
    else:
      avg_normed_avgs = norm_rts[0]
      dev_normed_avgs = (0,0)
    if not cat in cats:
      cats.append(cat)
    if not cat in bars:
      bars[cat] = []
      ebars[cat] = [[], []]
    bars[cat].append(avg_normed_avgs)
    ebars[cat][0].append(dev_normed_avgs[0])
    ebars[cat][1].append(dev_normed_avgs[1])
#    ebars[cat].append(dev_normed_avgs)

#for i in [4,5]:
#  bars[i].append(0)
#  ebars[i][0].append(0)
#  ebars[i][1].append(0)

# Plotting
fig = plt.figure(figsize=(20,4))

test = np.arange(len(bm_names))
width = 1.0 / float(num_setups + 1)
i = 0
colors = ['r', 'g', 'b', 'y', 'm', 'c', '0.5', '0.1', '0.7']

# define lables for categories
labels = []
for cnt, l in exp_idx["gromacs"].items():
  for param, exp in l.items():
    cat = exp % num_setups
    key_entry = str(cat) + ": %02d" % (cnt) + ", " + param
    labels.append(key_entry)
labels.sort()

print "CATs: %d" % (len(cats))
for cat in cats:
#  print norm_bars[cat]
#  if normalize:
  print "CAT %d:" % (cat)
  print "normalized BARs: %d" % (len(bars[cat]))
  print bars[cat]
  print "error BARs: %d" % (len(ebars[cat]))
  plt.bar(test+width*i, bars[cat], width, color=colors[i % len(colors)],
          yerr=ebars[cat][1], ecolor='k', label=labels[i])
#          yerr=ebars[cat], ecolor=colors[i % len(colors)], label=labels[i])
  i = i + 1

plt.xticks(test+width*(len(cats)/2.0), bm_names, rotation='vertical')
plt.xlim(0, len(bm_names))
plt.ylim(0, 7)

plt.legend(loc=2, labelspacing=0.1)

#plt.show()
plt.savefig("plots/new.pdf", format="pdf", bbox_inches='tight')
