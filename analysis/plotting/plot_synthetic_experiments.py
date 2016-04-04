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

colors = { 'michael': 'r', 'hammerthrow': 'g', 'caelum': 'b', 'hogun': 'c',
           'shark': 'm', 'tigger': 'y', 'uriel': '0.5' }

workload_labels = { 'cpu_spin.60s': "\\texttt{cpu\_spin}, 60s",
                    'mem_stream.1024B': "\\texttt{mem\_stream}, 1K",
                    'mem_stream.131072B': "\\texttt{mem\_stream}, 128K",
                    'mem_stream.1048576B': "\\texttt{mem\_stream}, 1M",
                    'mem_stream.52428800B': "\\texttt{mem\_stream}, 50M",
                    'io_stream.fio-seqread': "\\texttt{io\_stream}, seq.\ read.",
                    'io_stream.fio-seqwrite': "\\texttt{io\_stream}, seq.\ write."
                  }

machine_types = { 'hammerthrow': "A",
                  'decathlon': "A",
                  'freestyle': "A",
                  'backstroke': "A",
                  'hogun': "B",
                  'shark': "B",
                  'michael': "C",
                  'raphael': "C",
                  'uriel': "D",
                  'tigger': "E",
                  'caelum': "M" }

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
                        facecolor="white", edgecolor=median_color, lw=0.5)
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
        index_end = index_base + index_step * len(data) + 1
        indexed_data = zip(range(index_base, index_end, index_step), data)
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
        bp.draw_on(ax, index, box_color=color, median_color=color)

def print_overview(results_dict):
  for (wl, setup), hr in sorted(results_dict.items(), key=lambda x: x[0]):
    print "=================================================================="
    for host, v in hr.items():
      print "------------------------------------------------------------------"
      print "%s" % (host)
      print "=== %s.%s === (%d records)\n" % (wl, setup, len(v))
      print "IPC \t\t %s" % (get_dist_str(get_ipc(v)))
      print "CPI \t\t %s" % (get_dist_str(get_cpi(v)))
      print "IPMS \t\t %s" % (get_dist_str(get_ipms(v)))
      print "IPCR \t\t %s" % (get_dist_str(get_ipcr(v)))
      print "Miss ratio: \t %s" % (get_dist_str(get_cache_miss_ratio(v)))
      print "Runtime: \t %s" % (get_dist_str(get_runtime(v)))
      print

def best_median_runtime(results_dict):
  best_runtimes = {}
  for (wl, setup), hr in sorted(results_dict.items(), key=lambda x: x[0]):
    prev_best = 0.0
    for host, v in hr.items():
      if "caelum" in host:
        continue
      if prev_best == 0.0:
        prev_best = np.median(get_runtime(v))
      else:
        prev_best = min(prev_best, np.median(get_runtime(v)))
    best_runtimes[(wl, setup)] = prev_best
  return best_runtimes

def collect_data_for_metric(results_dict, data_dict, labels_vec, selector):
  for (wl, setup), hr in sorted(results_dict.items(), key=lambda x: x[0]):
    for host, v in hr.items():
      if host == "shark":
        continue
      if not host in data_dict:
        data_dict[host] = []
      data_vec = data_dict[host]
      data_vec.append(selector(v))
    labels_vec.append("%s.%s" % (wl, setup))

def translate_workload_name(wl):
  if wl in workload_labels:
    return workload_labels[wl]
  else:
    return wl

def translate_host_to_type(host):
  if host in machine_types:
    return machine_types[host]
  else:
    return host

def plot_box_whisker_chart(data, labels, ylabel, scale, outname, ylim=(-1, -1)):
  fig, ax = plt.subplots()
  i = 0
  for host, v in sorted(data.items(), key=lambda (k, v): machine_types[k]):
    bp = percentile_box_plot(ax, v, color=colors[host], index_base=i,
                             index_step=len(data))
    ax.plot(-1, -1, ls="-", marker=None, color=colors[host], lw=1.0,
            label="Type \\textbf{%s}" % (translate_host_to_type(host)))
    i += 1
  for i in range(0, len(data['michael'])):
    plt.axvline(i * len(data) + len(data) - 0.5, ls='-', color='k')

  ax.legend(frameon=False, loc="upper center", ncol=6,
            bbox_to_anchor=(0.0, 1.02, 1.0, 0.1), columnspacing=0.3)
  ax.set_xlabel('Workload')
  ax.set_ylabel(ylabel)
  if ylim == (-1, -1):
    if scale != "log":
      plt.ylim(ymin=0)
    else:
      plt.ylim(ymin=1)
  else:
    plt.ylim(ylim[0], ylim[1])
  plt.xlim(-0.5, len(data) * len(data['michael']) - 0.5)
  plt.xticks(np.arange(len(data) / 2.0, len(data) * len(labels), len(data)),
             [translate_workload_name(x) for x in labels], rotation=25,
             ha='right')
  plt.yscale(scale)

  #plt.setp(bp['whiskers'], color='k',  linestyle='-' )
  #plt.setp(bp['fliers'], markersize=3.0)
  plt.savefig(outname, format="pdf", bbox_inches='tight')

def collect_and_plot(perf_results, selector, ylabel, prefix, scale="linear",
                     ylim=(-1, -1)):
  data = {}
  labels = []
  collect_data_for_metric(perf_results, data, labels, selector)
  plot_box_whisker_chart(data, labels, ylabel, scale, "%s-%s" \
          % (prefix, outname), ylim)


if len(sys.argv) < 2:
  print "usage: plot_synthetic_experiments.py <input dir1> <input1 label> " \
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

data = []
labels = []
for d in inputdirs:
  print "====================================================================="
  print d

  perf_results = load_perf_files_from_dir(d)

  print_overview(perf_results)
  
  collect_and_plot(perf_results, get_ips, "Instructions per second", "ips", "log", ylim=(100000, 10000000000))
  collect_and_plot(perf_results, get_ipc, "Instructions per cycle", "ipc")
  collect_and_plot(perf_results, get_cpi, "Cycles per instruction", "cpi")
  collect_and_plot(perf_results, get_ipms, "Instructions per memory store",
                   "ipms", "log")
  collect_and_plot(perf_results, get_ipcr, "Instructions per cache reference",
                   "ipcr", "log")
  collect_and_plot(perf_results, get_ipcm, "Instructions per cache miss",
                   "ipcm", "log")
  collect_and_plot(perf_results, get_cache_miss_ratio, "Cache miss ratio",
                   "cmr", ylim=(0, 2))
  collect_and_plot(perf_results, get_runtime, "Runtime", "runtime")

  print best_median_runtime(perf_results)
