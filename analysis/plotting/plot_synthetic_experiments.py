#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import sys, re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from utils import *
from process_synthetic_experiments import *
from matplotlib import pylab
from scipy.stats import scoreatpercentile

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
                       facecolor="white",edgecolor=box_color)
        ax.broken_barh([(index - w2, width)],
                       (self.median,0),
                       facecolor="white", edgecolor=median_color)
        if self.whisk_top is not None:
            ax.broken_barh([(index - w2, width)],
                           (self.whisk_top,0),
                           facecolor="white", edgecolor=whisker_color)
            ax.broken_barh([(index , 0)],
                           (self.whisk_top, self.top-self.whisk_top),
                           edgecolor=box_color,linestyle="dashed")
        if self.whisk_bott is not None:
            ax.broken_barh([(index - w2, width)],
                           (self.whisk_bott,0),
                           facecolor="white", edgecolor=whisker_color)
            ax.broken_barh([(index , 0)],
                           (self.whisk_bott,self.bott-self.whisk_bott),
                           edgecolor=box_color,linestyle="dashed")
        if self.extreme_top is not None:
            ax.scatter([index], [self.extreme_top], marker='*')

def percentile_box_plot(ax, data, indexer=None, box_top=75,
                        box_bottom=25, whisker_top=99, whisker_bottom=1):
    if indexer is None:
        indexed_data = zip(range(1,len(data)+1), data)
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
        bp.draw_on(ax, index)

def print_overview(results_dict):
  for (wl, setup), v in sorted(results_dict.items(), key=lambda x: x[0]):
    print "----------------------------------------------------------------------"
    print "=== %s.%s === (%d records)\n" % (wl, setup, len(v))
    print "IPC \t\t %s" % (get_dist_str(get_ipc(v)))
    print "CPI \t\t %s" % (get_dist_str(get_cpi(v)))
    print "IPMS \t\t %s" % (get_dist_str(get_ipms(v)))
    print "IPCR \t\t %s" % (get_dist_str(get_ipcr(v)))
    print "Miss ratio: \t %s" % (get_dist_str(get_cache_miss_ratio(v)))
    print

def collect_data_for_metric(results_dict, data_vec, labels_vec, selector):
  for (wl, setup), v in sorted(results_dict.items(), key=lambda x: x[0]):
    data_vec.append(selector(v))
    labels_vec.append("%s.%s" % (wl, setup))

def plot_box_whisker_chart(data, labels, ylabel, scale, outname):
  fig, ax = plt.subplots()
  pos = np.array(range(len(data)))+1
  bp = percentile_box_plot(ax, data)

  #plt.legend(frameon=False)
  ax.set_xlabel('Workload')
  ax.set_ylabel(ylabel)
  if scale != "log":
    plt.ylim(ymin=0)
  else:
    plt.ylim(ymin=1)
  #plt.xlim(0, len(inputdirs) + 1)
  plt.xticks(range(1, len(labels) + 1), labels, rotation=45, ha='right')
  plt.yscale(scale)

  #plt.setp(bp['whiskers'], color='k',  linestyle='-' )
  #plt.setp(bp['fliers'], markersize=3.0)
  plt.savefig(outname, format="pdf", bbox_inches='tight')

def collect_and_plot(perf_results, selector, ylabel, prefix, scale="linear"):
  data = []
  labels = []
  collect_data_for_metric(perf_results, data, labels, selector)
  plot_box_whisker_chart(data, labels, ylabel, scale, "%s-%s" \
          % (prefix, outname))


if len(sys.argv) < 2:
  print "usage: plot_synthetic_experiments.py <input dir1> <input1 label> " \
        "<input dir2> <input2 label> ... <output file>"
  sys.exit(1)

#set_rcs()

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

data = []
labels = []
for d in inputdirs:
  print "====================================================================="
  print d

  perf_results = load_perf_files_from_dir(d)

  print_overview(perf_results)
  
  collect_and_plot(perf_results, get_ipc, "Instructions per cycle", "ipc")
  collect_and_plot(perf_results, get_cpi, "Cycles per instruction", "cpi")
  collect_and_plot(perf_results, get_ipms, "Instructions per memory store", "ipms", "log")
  collect_and_plot(perf_results, get_ipcr, "Instructions per cache reference", "ipcr", "log")
  collect_and_plot(perf_results, get_cache_miss_ratio, "Cache miss ratio", "cmr")
