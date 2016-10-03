# Copyright (c) 2016, Malte Schwarzkopf

import csv
import gflags
import math
import matplotlib
matplotlib.use("agg")
import os, sys
import matplotlib.pyplot as plt
from utils import *
from box_and_whisker import *

FLAGS = gflags.FLAGS
gflags.DEFINE_bool('paper_mode', False, 'Adjusts the size of the plots.')
gflags.DEFINE_string('trace_paths', '',
                     ', separated list of path to trace files.')
gflags.DEFINE_string('trace_labels', '',
                     ', separated list of labels to use for trace files.')
gflags.DEFINE_integer('ignore_runs_before', 0,
                      'timestamp before which scheduler runs are ignored')

def get_total_runtime(trace_path):
    csv_file = open(trace_path + "/scheduler_events/scheduler_events.csv")
    csv_reader = csv.reader(csv_file)
    runtimes = []
    for row in csv_reader:
      ts = long(row[0])
      if ts >= FLAGS.ignore_runs_before:
        runtimes.append(long(row[3]) / 1000000.0)
    csv_file.close()
    return runtimes


def plot_scalability(plot_file_name, setups, runtimes,
                     x_label="Cluster size [machines]",
                     y_label="Algorithm runtime [sec]"):
    if FLAGS.paper_mode:
        plt.figure(figsize=(3.33, 2.22))
        set_paper_rcs()
    else:
        plt.figure()
        set_rcs()

    ax = plt.gca()
    bp = percentile_box_plot(ax, runtimes, color='b')

    #plt.errorbar(range(1, len(setups) + 1), [np.mean(x) for x in runtimes],
    #             yerr=[np.std(x) for x in runtimes], marker="x")
    plt.xlim(0.5, len(setups) + 0.5)
    plt.ylim(0, 103)
    plt.xticks(range(1, len(setups) + 1),
               ["%u" % (round(float(x) * 12500)) for x in setups],
               rotation=30, ha='right')
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    plt.savefig("%s.pdf" % plot_file_name,
                format="pdf", bbox_inches="tight", pad_inches=0.002)


def main(argv):
    try:
        argv = FLAGS(argv)
    except gflags.FlagsError as e:
        print('%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS))

    trace_paths = FLAGS.trace_paths.split(',')
    labels = FLAGS.trace_labels.split(',')

    runtimes = []
    for t in trace_paths:
        trace_runtimes = get_total_runtime(t)
        runtimes.append(trace_runtimes)
        print t, np.mean(trace_runtimes)
    plot_scalability('quincy_scalability', labels, runtimes)


if __name__ == '__main__':
  main(sys.argv)
