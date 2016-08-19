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
import process_mesos_masterlog
from baselines import *

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

setup_labels = { "simple": "Random",
                 "whare-m": "Firmament/Whare-M",
                 "whare-mcs": "Firmament/Whare-MCs",
                 "coco": "Firmament",
                 "mesos": "Mesos",
                 "k8s" : "Kubernetes" }

#colors = { 'simple': '0.5', 'whare-mcs': 'r', 'mesos': 'b', 'coco': 'g' }
colors = [ '0.5', 'b', 'r', 'g', 'y', 'c', 'm', 'k' ]

setup_colors = { "simple": "0.5",
                 "whare-m": "y",
                 "whare-mcs": "r",
                 "coco": "g",
                 "mesos": "b",
                 "k8s" : "c" }

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
        bp.draw_on(ax, index, box_color=color, median_color=color,
                   whisker_color=color)

def print_overview(results_dict):
  for wl, v in sorted(results_dict["runtimes"].items(), key=lambda x: x[0]):
    #print "======================================================================"
    print "=== %s === (%d records)" % (wl, len(v))
    #print "IPC \t\t %s" % (get_dist_str(get_ipc(v)))
    if (len(results['cpi']) > 0):
      print "CPI \t\t %s" % (get_dist_str(results["cpi"][wl]))
    if (len(results['ipma']) > 0):
      print "IPMA: \t\t %s" % (get_dist_str(results["ipma"][wl]))
    #print "LLC miss ratio:  %s" % (get_dist_str(results["cache-misses"][wl]))
    if (len(v) > 0):
      print "Runtime: \t %s" % (get_dist_str(v))
    if (len(results['waittimes']) > 0):
      print "Wait time: \t %s" % (get_dist_str(results['waittimes'][wl]))
    #print "----------------------------------------------------------------------"

# XXX(malte): nasty hack to get custom sorting order...
def workload_sort(wl):
  if "cpu" in wl:
    return 0
  elif "mem_stream" in wl:
    return 1
  elif "io_stream" in wl:
    if "read" in wl:
      return 2
    else:
      return 3
  else:
    return wl

def collect_data_for_metric(results_dict, data_dict, labels_vec):
  first = True
  for setup, wls in sorted(results_dict.items(), key=lambda x: x[0]):
    if not setup in data_dict:
      data_dict[setup] = []
    for wl, v in sorted(wls.items(), key=lambda x: workload_sort(x[0])):
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

def translate_setup_name(setup):
  if setup in setup_labels:
    return setup_labels[setup]
  else:
    return setup

def plot_box_whisker_chart(data, setups, labels, ylabel, scale, outname,
                           ylim=(-1, -1), normed=False):
  fig, ax = plt.subplots(figsize=(6, 4))
  i = 0
  data_len = 3

  for setup, v in sorted(data.items(), key=lambda k: setups.index(k[0])):
    bp = percentile_box_plot(ax, v, color=colors[i], index_base=i,
                             index_step=data_len)
    plt.plot(-1, -1, label=translate_setup_name(setup), color=colors[i],
             lw=1.0)
    i += 1
  for i in range(0, len(data['simple'])):
    plt.axvline(i * data_len + data_len - 0.5, ls='-', color='k')

  ax.legend(frameon=False, loc="upper center", ncol=6,
            bbox_to_anchor=(0.0, 1.02, 1.0, 0.1), handletextpad=0.2,
            columnspacing=0.2)
  #ax.set_xlabel('Workload')
  ax.set_ylabel(ylabel)
  if ylim == (-1, -1):
    if scale != "log":
      plt.ylim(ymin=0)
    else:
      plt.ylim(ymin=1)
  else:
    plt.ylim(ylim[0], ylim[1])
  plt.xlim(-0.5, data_len * (len(data['simple']) - 1) + data_len - 0.5)
  plt.xticks(np.arange(data_len / 2.0, data_len * len(labels), data_len),
             [translate_workload_name(x) for x in labels], rotation=15,
             ha='right')
  plt.yscale(scale)
  if normed:
    plt.axhline(1.0, ls='-', color='k', lw=1.0)
    ax.set_yticklabels(["%d$\\times$" % (x) for x in ax.get_yticks()])

  #plt.setp(bp['whiskers'], color='k',  linestyle='-' )
  #plt.setp(bp['fliers'], markersize=3.0)
  plt.savefig(outname, format="pdf", bbox_inches='tight')

def plot_cdf(data, xlabel, out_prefix, outname, xlim=(-1, -1)):
  plt.clf()
  i = 0
  for setup, sd in data.items():
    all_cpi_values_for_setup = []
    for wl, v in sd.items():
      all_cpi_values_for_setup.extend(v)
    (n, bins, patches) = plt.hist(all_cpi_values_for_setup,
             bins=np.linspace(min(all_cpi_values_for_setup),
                              max(all_cpi_values_for_setup), 10000),
             histtype="step", cumulative=True, normed=True, lw=1.0,
             label=translate_setup_name(setup),
             color=setup_colors[setup])
    # hack to remove vertical bar
    patches[0].set_xy(patches[0].get_xy()[:-1])
    i += 1
  if xlim != (-1, -1):
    plt.xlim(xmin=xlim[0], xmax=xlim[1])
  plt.ylim(0, 1.0)
  plt.ylabel("CDF")
  plt.xlabel(xlabel)
  plt.legend(frameon=False, loc="best")
  plt.savefig("%s-%s" % (out_prefix, outname), format="pdf",
              bbox_inches="tight")

def collect_and_plot(perf_results, setups, ylabel, prefix, scale="linear",
                     ylim=(-1, -1), normed=False):
  data = {}
  labels = []
  collect_data_for_metric(perf_results, data, labels)
  plot_box_whisker_chart(data, setups, labels, ylabel, scale, "%s-%s" \
          % (prefix, outname), ylim, normed)

def normalize_by_baseline(workload, runtime, cluster="srg"):
  if cluster == "srg":
    normed = runtime / baseline_best_medians[workload]
    if normed < 0.9:
      print "WARNING: low normalized runtime for %s: %f (%f)" % (workload, runtime, normed)
    return normed
  elif cluster == "caelum":
    normed = runtime / baseline_caelum_medians[workload]
    if normed < 0.9:
      print "WARNING: low normalized runtime for %s: %f (%f)" % (workload, runtime, normed)
    return normed
  else:
    print "unknown cluster!"
    sys.exit(1)

def get_cpi(td, ls):
  if 'final_report' in td:
    if 'cycles' in td['final_report']:
      cpi = float(td['final_report']['cycles']) / float(td['final_report']['instructions'])
    else:
      print "WARNING: missing CPI value for task %u" % (td['uid'])
      cpi = 0.0
    if cpi > 0.0:
      ls.append(cpi)
  for c in td['spawned']:
    get_cpi(c, ls)

def get_cache_misses(td, ls):
  if 'final_report' in td:
    if 'llc_misses' in td['final_report']:
      miss_ratio = float(td['final_report']['llc_misses']) / float(td['final_report']['llc_refs'])
    else:
      print "WARNING: missing LLC miss count value for task %u" % (td['uid'])
      miss_ratio = 0.0
    if miss_ratio > 0.0:
      ls.append(miss_ratio)
  for c in td['spawned']:
    get_cache_misses(c, ls)

def get_ipma(td, ls):
  if 'final_report' in td:
    if 'instructions' in td['final_report']:
      ipma = float(td['final_report']['instructions']) / float(td['final_report']['llc_misses'])
    else:
      print "WARNING: missing instruction count value for task %u" % (td['uid'])
      ipma = 0.0
    if ipma > 0.0:
      ls.append(ipma)
  for c in td['spawned']:
    get_ipma(c, ls)

def get_runtimes(td, ls):
  #if 'final_report' in td:
  #  runtime = float(td['final_report']['runtime'])
  #  if runtime > 0.0:
  #    ls.append(runtime)
  runtime = get_runtime(td)
  if runtime > 0.0:
    ls.append(get_runtime(td))
  #  ls.append(to_seconds(get_runtime(td)))
  for c in td['spawned']:
    get_runtimes(c, ls)

def get_runtime(td):
  if not 'finish_time' in td or td['state'] != 5:
    return 0.0
  #rt = int(td['finish_time']) - int(td['start_time'])
  rt = float(td['final_report']['runtime'])
  if rt <= 0:
    print "WARNING: zero or negative runtime found for task %d: " \
            "%dus" % (int(td['uid']), rt)
  return rt

def get_waittimes(td, ls):
  waittime = get_waittime(td)
  if waittime > 0.0:
    ls.append(get_waittime(td))
  #  ls.append(to_seconds(get_runtime(td)))
  for c in td['spawned']:
    get_waittimes(c, ls)

def get_waittime(td):
  if not 'start_time' in td or td['state'] != 5:
    print "WARNING: looks like task %d never scheduled!" % (int(td['uid']))
    return -1.0
  # Timestamps are in microseconds
  wt = (float(td['start_time']) - float(td['submit_time'])) / 1000000.0
  if wt <= 0:
    print "WARNING: zero or negative wait time found for task %d: " \
            "%dus" % (int(td['uid']), wt)
  return wt

def to_seconds(time):
  return time / 1000000.0

def load_workload_data_from_dir(directory, setup):
  if "caelum" in directory:
    cluster = "caelum"
  else:
    cluster = "srg"
  workload_runtimes = {}
  workload_waittimes = {}
  workload_cpi = {}
  workload_cache_misses = {}
  workload_ipma = {}
  for subdir, dirs, files in os.walk(directory):
    if "logs" in subdir:
      continue
    for file in files:
      workload = subdir[subdir.rfind("/") + 1:-1]
      with open(os.path.join(subdir, file)) as fd:
        data = json.load(fd)
      if not workload in workload_runtimes:
        workload_runtimes[workload] = []
        workload_waittimes[workload] = []
        workload_cpi[workload] = []
        workload_cache_misses[workload] = []
        workload_ipma[workload] = []
      root_td = data['root_task']
      get_runtimes(root_td, workload_runtimes[workload])
      get_waittimes(root_td, workload_waittimes[workload])
      get_cpi(root_td, workload_cpi[workload])
      get_cache_misses(root_td, workload_cache_misses[workload])
      get_ipma(root_td, workload_ipma[workload])

  # normalize by baseline
  normalized_workload_runtimes = {}
  for wl, rts in workload_runtimes.items():
    normalized_workload_runtimes[wl] = [normalize_by_baseline(wl, rt, cluster) for rt in rts]
  return { 'runtimes': normalized_workload_runtimes, 'cpi': workload_cpi,
           'cache-misses': workload_cache_misses, 'ipma': workload_ipma,
           'waittimes': workload_waittimes }


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

runtime_data = {}
waittime_data = {}
cpi_data = {}
ipma_data = {}
cache_miss_data = {}
i = 0
for d in inputdirs:
  print "====================================================================="
  print d

  if not "mesos" in labels[i]:
    results = load_workload_data_from_dir(d, labels[i])
    print_overview(results)
    runtime_data[labels[i]] = results['runtimes']
    waittime_data[labels[i]] = results['waittimes']
    cpi_data[labels[i]] = results['cpi']
    ipma_data[labels[i]] = results['ipma']
    cache_miss_data[labels[i]] = results['cache-misses']
  elif "mesos" in labels[i]:
    if "caelum" in d:
      cluster = "caelum"
    else:
      cluster = "srg"
    # Mesos only supplies runtime information
    raw_runtimes, raw_waittimes = process_mesos_masterlog.parse_master_log("%s/mesos-master.INFO" % (d))
    normalized_workload_runtimes = {}
    for wl, rts in raw_runtimes.items():
      normalized_workload_runtimes[wl] = [normalize_by_baseline(wl, rt, cluster) for rt in rts]
    print_overview({ 'runtimes': normalized_workload_runtimes })
    runtime_data[labels[i]] = normalized_workload_runtimes
    waittime_data[labels[i]] = raw_waittimes
  else:
    print "Unknown setup!"
    sys.exit(1)

  i += 1

collect_and_plot(runtime_data, labels, "Normalized runtime", "normed-runtime", ylim=(0, 5), normed=True)
collect_and_plot(waittime_data, labels, "Wait time [sec]", "waittime-lin", scale="linear")
collect_and_plot(waittime_data, labels, "Wait time [sec]", "waittime-log", scale="log", ylim=(0.1, 100))
plot_cdf(cpi_data, "Cycles per instruction", "cpi-cdf", outname, xlim=(0, 5))
plot_cdf(waittime_data, "Wait time", "waittime-cdf", outname)
#plot_cdf(cache_miss_data, "Cache miss fraction", "cache-miss", outname)
plot_cdf(ipma_data, "Instructions per memory access", "ipma", outname, xlim=(0, 10000))

#  collect_and_plot(results, labels, get_ips, "Instructions per second", "ips")
#  collect_and_plot(results, labels, get_ipc, "Instructions per cycle", "ipc")
#  collect_and_plot(results, labels, get_cpi, "Cycles per instruction", "cpi")
#  collect_and_plot(results, labels, get_cache_miss_ratio, "Cache miss ratio", "cmr", ylim=(0, 2))
