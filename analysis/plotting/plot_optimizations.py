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
gflags.DEFINE_bool('log_scale', False, '')

def plot_scalability(plot_file_name, runtimes, xlabel, x_labels, y_label,
                     given_color):
    if FLAGS.paper_mode:
        plt.figure(figsize=(1.4, 0.93))
        set_paper_rcs()
    else:
        plt.figure()
        set_rcs()

    ax = plt.gca()
    bp = percentile_box_plot(ax, runtimes, color=given_color)

    #plt.errorbar(range(1, len(setups) + 1), [np.mean(x) for x in runtimes],
    #             yerr=[np.std(x) for x in runtimes], marker="x")
    plt.xlim(0.5, len(x_labels) + 0.5)
    plt.ylim(ymin=0)
    plt.xticks(range(1, len(x_labels) + 1), x_labels, ha='center')
    plt.yticks(range(0, 60000001, 15000000), range(0, 61, 15))
    plt.ylabel(y_label)
    plt.xlabel(xlabel)
    plt.savefig("%s.pdf" % plot_file_name,
                format="pdf", bbox_inches="tight")


def get_cost_scaling_optimization_runtimes(trace_path, column_index):
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


def get_relax_optimization_runtimes(trace_path, column_index):
    # 0 timestamp
    # 1 solver runtime
    # 2 algorithm runtime
    # 3 total runtime (including Firmament)
    runtimes = []
    csv_file = open(trace_path + "/scheduler_events/scheduler_events.csv")
    csv_reader = csv.reader(csv_file)
    index = 0
    for row in csv_reader:
        timestamp = long(row[0])
        if timestamp > FLAGS.runtimes_after_timestamp:
            if index % 2 == 0:
                runtimes.append(long(row[column_index]))
            index = index + 1
    csv_file.close()
    return runtimes


def main(argv):
    try:
        argv = FLAGS(argv)
    except gflags.FlagsError as e:
        print('%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS))

    trace_paths = FLAGS.trace_paths.split(',')
    labels = FLAGS.trace_labels.split(',')
    algo_runtimes = []
    algo_trace_labels = []
    trace_id = 0
    xlabel = ''
    given_color = ''
    for trace_path in trace_paths:
        algo_runtime = []
        if 'relax' in trace_path:
            algo_runtime = get_relax_optimization_runtimes(trace_path, 2)
            xlabel = 'Relaxation'
            given_color = 'g'
        elif 'cost_scaling' in trace_path:
            algo_runtime = get_cost_scaling_optimization_runtimes(trace_path, 2)
            xlabel = 'Cost scaling'
            given_color = 'b'
        # XXX(malte): hack to deal with cs2 not providing this info
        if algo_runtime[0] != 18446744073709551615:
          algo_runtimes.append(algo_runtime)
          algo_trace_labels.append(labels[trace_id])
        trace_id += 1
    print algo_runtimes
    plot_scalability('optimizations_box_and_whiskers',
                     algo_runtimes, xlabel, labels,
                     "Alg. runtime [sec]", given_color)


if __name__ == '__main__':
  main(sys.argv)
