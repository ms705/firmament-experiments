#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import sys, re, json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from utils import *
from process_synthetic_experiments import *
from matplotlib import pylab
from scipy.stats import scoreatpercentile

baseline_best_medians = { 'mem_stream_1M_': 55.649999999999999,
                          'mem_stream_128K_': 55.590000000000003, 
                          'mem_stream_50M_': 56.990000000000002,
                          'io_stream_read': 73.510000000000005,
                          'mem_stream_1K': 52.939999999999998,
                          'io_stream_write': 29.620000000000001,
                          'cpu_spin': 60.0
                        }

workload_labels = { 'cpu_spin': "\\texttt{cpu\_spin}, 60s", 
                    'mem_stream.1K': "\\texttt{mem\_stream}, 1K",
                    'mem_stream.128K': "\\texttt{mem\_stream}, 128K",
                    'mem_stream_1M_': "\\texttt{mem\_stream}, 1M",
                    'mem_stream_50M_': "\\texttt{mem\_stream}, 50M",
                    'io_stream_read': "\\texttt{io\_stream}, seq.\ read.",
                    'io_stream_write': "\\texttt{io\_stream}, seq.\ write."
                  }

colors = { 'simple': '0.5', 'whare-mcs': 'r' }

# @author: Aaron Blankstein, with modifications by Malte Schwarzkopf
class boxplotter(object):
    def __init__(self, median, top, bottom, whisk_top=None,
                 whisk_bottom=None, extreme_top=None):
        self.median = median
        self.top = top
        self.bott = bottom
        self.whisk_top = whisk_top
        self.whisk_bott = whisk_bottom
        self.extreme_top = extreme_top
    def draw_on(self, ax, index, box_color = "blue",
                median_color = "red", whisker_color = "black"):
        width = .7
        w2 = width / 2
        ax.broken_barh([(index - w2, width)],
                       (self.bott,self.top - self.bott),
                        facecolor="white", edgecolor=box_color, lw=0.5)
        ax.broken_barh([(index - w2, width)],
                        (self.median,0),
                        facecolor="white", edgecolor=median_color, lw=1.0)
        if self.whisk_top is not None:
            ax.broken_barh([(index - w2, width)],
                           (self.whisk_top,0),
                            facecolor="white", edgecolor=whisker_color, lw=0.5)
            ax.broken_barh([(index , 0)],
                           (self.whisk_top, self.top-self.whisk_top),
                            edgecolor=box_color,linestyle="dashed", lw=0.5)
        if self.whisk_bott is not None:
            ax.broken_barh([(index - w2, width)],
                           (self.whisk_bott,0),
                            facecolor="white", edgecolor=whisker_color, lw=0.5)
            ax.broken_barh([(index , 0)],
                           (self.whisk_bott,self.bott-self.whisk_bott),
                            edgecolor=box_color, linestyle="dashed", lw=0.5)
        if self.extreme_top is not None:
            ax.scatter([index], [self.extreme_top], marker='*',
                        edgecolor=box_color, facecolor=box_color, lw=0.5)

def percentile_box_plot(ax, data, indexer=None, index_base=1, index_step=1,
                        box_top=75, box_bottom=25, whisker_top=99,
                        whisker_bottom=1, color='k', label=""):
    if indexer is None:
        indexed_data = zip(range(index_base, index_base + index_step * len(data) + 1, index_step), data)
    else:
        indexed_data = [(indexer(datum), datum) for datum in data]
    def get_whisk(vector, w):
        if w is None:
            return None
        return scoreatpercentile(vector, w)

    for index, x in indexed_data:
        bp = boxplotter(scoreatpercentile(x, 50),
                        scoreatpercentile(x, box_top),
                        scoreatpercentile(x, box_bottom),
                        get_whisk(x, whisker_top),
                        get_whisk(x, whisker_bottom),
                        scoreatpercentile(x, 100))
        bp.draw_on(ax, index, box_color=color, median_color=color, whisker_color=color)

def print_overview(results_dict):
  for wl, v in sorted(results_dict.items(), key=lambda x: x[0]):
    #print "======================================================================"
    print "=== %s === (%d records)" % (wl, len(v))
    #print "IPC \t\t %s" % (get_dist_str(get_ipc(v)))
    #print "CPI \t\t %s" % (get_dist_str(get_cpi(v)))
    #print "Cache miss ratio: \t %s" % (get_dist_str(get_runtime(v)))
    print "Runtime: \t %s" % (get_dist_str(v))
    #print "----------------------------------------------------------------------"

def collect_data_for_metric(results_dict, data_dict, labels_vec):
  first = True
  for setup, wls in sorted(results_dict.items(), key=lambda x: x[0]):
    if not setup in data_dict:
      data_dict[setup] = []
    for wl, v in wls.items():
      data_vec = data_dict[setup]
      data_vec.append(v)
      if first:
        labels_vec.append("%s" % (wl))
    first = False

def translate_workload_name(wl):
  if wl in workload_labels:
    return workload_labels[wl]
  else:
    return wl

def plot_box_whisker_chart(data, labels, ylabel, scale, outname, ylim=(-1, -1)):
  fig, ax = plt.subplots()
  i = 0
  for setup, v in data.items():
    bp = percentile_box_plot(ax, v, color=colors[setup], index_base=i,
                             index_step=len(data))
    plt.plot(-1, -1, label=setup, color=colors[setup], lw=1.0)
    i += 1
  for i in range(0, len(data['simple'])):
    plt.axvline(i * len(data) + len(data) - 0.5, ls='-', color='k')

  ax.legend(frameon=False, loc="upper center", ncol=6,
            bbox_to_anchor=(0.0, 1.02, 1.0, 0.1))
  ax.set_xlabel('Workload')
  ax.set_ylabel(ylabel)
  if ylim == (-1, -1):
    if scale != "log":
      plt.ylim(ymin=0)
    else:
      plt.ylim(ymin=1)
  else:
    plt.ylim(ylim[0], ylim[1])
  plt.axhline(1.0, ls='--', color='k')
  plt.xlim(-0.5, len(data) * len(labels) + 0.5)
  plt.xticks(np.arange(len(data) / 2.0, len(data) * len(labels), len(data)),
             [translate_workload_name(x) for x in labels], rotation=45,
             ha='right')
  plt.yscale(scale)
  ax.set_yticklabels(["%d\\times" % (x) for x in ax.get_yticks()])

  #plt.setp(bp['whiskers'], color='k',  linestyle='-' )
  #plt.setp(bp['fliers'], markersize=3.0)
  plt.savefig(outname, format="pdf", bbox_inches='tight')

def collect_and_plot(perf_results, ylabel, prefix, scale="linear",
                     ylim=(-1, -1)):
  data = {}
  labels = []
  collect_data_for_metric(perf_results, data, labels)
  plot_box_whisker_chart(data, labels, ylabel, scale, "%s-%s" \
          % (prefix, outname), ylim)

def normalize_by_baseline(workload, runtime):
  return runtime / baseline_best_medians[workload]

def get_runtimes(td, ls):
  runtime = get_runtime(td)
  if runtime > 0.0:
    ls.append(to_seconds(get_runtime(td)))
  for c in td['spawned']:
    get_runtimes(c, ls)

def get_runtime(td):
  if not 'finish_time' in td:
    return 0.0
  rt = int(td['finish_time']) - int(td['start_time'])
  if rt <= 0:
    print "WARNING: zero or negative runtime found for task %d: " \
            "%dus" % (int(td['uid']), rt)
  return rt

def to_seconds(time):
  return time / 1000000.0

def load_workload_data_from_dir(directory, setup):
  workload_runtimes = {}
  for subdir, dirs, files in os.walk(directory):
    if "logs" in subdir:
      continue
    for file in files:
      workload = subdir[subdir.rfind("/") + 1:-1]
      with open(os.path.join(subdir, file)) as fd:
        data = json.load(fd)
      if not workload in workload_runtimes:
        workload_runtimes[workload] = []
      root_td = data['root_task']
      get_runtimes(root_td, workload_runtimes[workload])

  # normalize by baseline
  normalized_workload_runtimes = {}
  for wl, rts in workload_runtimes.items():
    normalized_workload_runtimes[wl] = [normalize_by_baseline(wl, rt) for rt in rts]
  return normalized_workload_runtimes
 

############################################################################

if len(sys.argv) < 2:
  print "usage: plot_cluster_mix.py <input dir1> <input1 label> " \
        "<input dir2> <input2 label> ... <output file>"
  sys.exit(1)

set_rcs()

# arg processing
if (len(sys.argv) - 1) % 2 == 1:
  # odd number of args, have output name
  outname = sys.argv[-1]
  print "Output name specified: %s" % (outname)
else:
  print "Please specify an output name!"
  sys.exit(1)

inputdirs = []
labels = []
for i in range(1, len(sys.argv)-1, 2):
  inputdirs.append(sys.argv[i])
  labels.append(sys.argv[i+1])

data = {}
i = 0
for d in inputdirs:
  print "====================================================================="
  print d

  results = load_workload_data_from_dir(d, labels[i])
  print_overview(results)
  data[labels[i]] = results
  i += 1

collect_and_plot(data, "Normalized runtime", "normed-runtime", ylim=(0, 5))

#  collect_and_plot(results, get_ips, "Instructions per second", "ips")
#  collect_and_plot(results, get_ipc, "Instructions per cycle", "ipc")
#  collect_and_plot(results, get_cpi, "Cycles per instruction", "cpi")
#  collect_and_plot(results, get_cache_miss_ratio, "Cache miss ratio", "cmr", ylim=(0, 2))
