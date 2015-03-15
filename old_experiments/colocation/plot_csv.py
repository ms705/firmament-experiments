# Script to plot the results of all pair program interference.

import sys
import math
import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import pylab
from matplotlib.colors import LogNorm

def usage():
  print "plot_csv.py <isolation csv file> <colocation csv file> <filter cpu num>"

if len(sys.argv) < 4:
  usage()
  sys.exit()

iso_file = sys.argv[1]
col_file = sys.argv[2]
cpu_num = sys.argv[3]

num_baselines = {}
baselines = {}
for line in open(iso_file).readlines():
  vals = re.split(',', line.strip())
  if baselines.has_key(vals[0]):
    baselines[vals[0]] += float(vals[1])
    num_baselines[vals[0]] += 1
  else:
    baselines[vals[0]] = float(vals[1])
    num_baselines[vals[0]] = 1

# Compute average of the baselines / task type
for bs in baselines:
  baselines[bs] /= num_baselines[bs]

benchmarks = {'ab': 0, 'quick_sort': 1, 'page_rank': 2, 'binoptions': 3,
              'shark': 4}

num_vals = np.zeros([len(benchmarks), len(benchmarks)], dtype=float)
avg_vals = np.zeros([len(benchmarks), len(benchmarks)], dtype=float)
norm_vals = np.zeros([len(benchmarks), len(benchmarks)], dtype=float)
std_dev = np.zeros([len(benchmarks), len(benchmarks)], dtype=float)

for line in open(col_file).readlines():
    vals = re.split(',', line.strip())
    if vals[1] == cpu_num:
      i = benchmarks[vals[2]]
      j = benchmarks[vals[3]]
      num_vals[i][j] += 1
      num_vals[j][i] += 1
      avg_vals[i][j] += float(vals[4])
      avg_vals[j][i] += float(vals[8])

bmarks = ['ab', 'quick_sort', 'page_rank', 'binoptions', 'shark']
bmark_labels = ['HTTP', 'QS', 'PR', 'BOPM', 'SQ']

print "Normalized run times:"
# Compute normalized run times
for i in  bmarks:
  line = i + " "
  for j in bmarks:
    b1 = benchmarks[i]
    b2 = benchmarks[j]
    if num_vals[b1][b2] != 0:
      avg_vals[b1][b2] /= num_vals[b1][b2]
    norm_vals[b1][b2] = avg_vals[b1][b2] / baselines[i]
    line += str(norm_vals[b1][b2]) + " "
  print line

print "Standard deviation:"
# Compute stdev
for line in open(col_file).readlines():
  vals = re.split(',', line.strip())
  if vals[1] == cpu_num:
    i = benchmarks[vals[2]]
    j = benchmarks[vals[3]]
    std_dev[i][j] += (float(vals[4]) - avg_vals[i][j]) * (float(vals[4]) - avg_vals[i][j])
    std_dev[j][i] += (float(vals[8]) - avg_vals[j][i]) * (float(vals[8]) - avg_vals[j][i])
for i in  bmarks:
  line = i + " "
  for j in bmarks:
    b1 = benchmarks[i]
    b2 = benchmarks[j]
    if num_vals[b1][b2] != 0:
      std_dev[b1][b2] /= num_vals[b1][b2]
      std_dev[b1][b2] = math.sqrt(std_dev[b1][b2])
    line += str(std_dev[b1][b2]) + " "
  print line

# Plotting
fig = plt.figure(figsize=(2,2))
pylab.rc('font', size='8.0')

#plt.matshow(norm_vals, vmax=2.0, vmin=0.0)
plt.matshow(norm_vals, vmin=0.9, fignum=0, cmap='spectral')
#            norm=LogNorm(vmin=0.9, vmax=2.2))

cb = plt.colorbar(shrink=0.8, format='%1.1f$\\times$', ticks=[1.0, 1.2, 1.4,
                                                              1.6, 1.8, 2.0, 2.2])
cb.set_label('Normalized runtime')

plt.xticks(np.arange(len(bmarks)), bmark_labels)
for tick in pylab.gca().xaxis.iter_ticks():
  tick[0].label2On = True
  tick[0].label1On = False
  tick[0].label2.set_rotation(45)
plt.yticks(np.arange(len(bmarks)), bmark_labels)
plt.xlim(-0.5, len(baselines)-0.5)
plt.ylim(-0.5, len(baselines)-0.5)

#plt.show()
plt.savefig("col-4-%s.pdf" % cpu_num, format="pdf", bbox_inches='tight')
plt.savefig("col-4-%s.png" % cpu_num, format="png", bbox_inches='tight')


'''
  plt.suptitle(runtimes.keys()[i], y=0.1)
  plt.savefig("plots/ap-new-%d-fs.pdf" % i, format="pdf", bbox_inches='tight')
  plt.savefig("plots/ap-new-%d-fs.png" % i, format="png", bbox_inches='tight')
'''
