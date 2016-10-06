# Copyright (c) 2016, Ionel Gog

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
gflags.DEFINE_integer('runtimes_after_timestamp', 0,
                      'Only plot runtimes of runs that happened after.')

def get_scheduler_runtimes(trace_path, column_index):
    # 0 timestamp
    # 1 solver runtime
    # 2 algorithm runtime
    # 3 total runtime (including Firmament)
    runtimes = []
    csv_file = open(trace_path + "/scheduler_events/scheduler_events.csv")
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        timestamp = long(row[0])
        if timestamp > FLAGS.runtimes_after_timestamp:
            runtimes.append(long(row[column_index]))
    csv_file.close()
    runtimes.sort()
    return runtimes

def plot_runtimes(runtimes, labels):
    colors = ['y', 'b', 'm', 'b', 'm']
    if FLAGS.paper_mode:
        plt.figure(figsize=(3, 2))
        set_paper_rcs()
    else:
        plt.figure()
        set_rcs()
    ax = plt.gca()
    bp = percentile_box_plot(ax, runtimes, color=colors, box_lw=1.0,
                             median_lw=1.5)
    plt.plot(-1, -1, label='Cost scaling', color='b', lw=1.0)
    plt.plot(-1, -1, label='Incremental cost scaling', color='m', lw=1.0)

    for i in range(2, len(runtimes), 2):
        plt.axvline(i + 0.5, ls='-', color='k')

    ax.legend(frameon=False, loc="upper center", ncol=6,
              bbox_to_anchor=(0.0, 1.04, 1.0, 0.1), handletextpad=0.2,
              columnspacing=0.2)

    plt.xlim(0.5, 2 * len(labels) + 0.5)
    plt.xticks([x * 2 + 1.5 for x in range(0, len(labels))], labels)
    plt.ylim(0, 60000000)
    plt.yticks(range(0, 60000001, 10000000), range(0, 61, 10))
    plt.xlabel("Scheduling policy")
    plt.ylabel("Algorithm runtime [sec]")
    plt.savefig("incremental_cost_scaling_box_whiskers.pdf",
                format="pdf", bbox_inches="tight", pad_inches=0.003)



def main(argv):
    try:
        argv = FLAGS(argv)
    except gflags.FlagsError as e:
        print('%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS))

    trace_paths = FLAGS.trace_paths.split(',')
    labels = FLAGS.trace_labels.split(',')
    algo_runtimes = []
    trace_id = 0
    for trace_path in trace_paths:
        algo_runtime = get_scheduler_runtimes(trace_path, 2)
        algo_runtimes.append(algo_runtime)

    plot_runtimes(algo_runtimes, labels)


if __name__ == '__main__':
  main(sys.argv)
