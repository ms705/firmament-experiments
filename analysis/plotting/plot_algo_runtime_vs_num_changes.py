# Copyright (c) 2016, Ionel Gog

import csv
import gflags
import math
import matplotlib
matplotlib.use("agg")
import os, sys
import matplotlib.pyplot as plt
from utils import *

FLAGS = gflags.FLAGS
gflags.DEFINE_bool('paper_mode', False, 'Adjusts the size of the plots.')
gflags.DEFINE_string('trace_paths', '',
                     ', separated list of path to trace files.')
gflags.DEFINE_string('trace_labels', '',
                     ', separated list of labels to use for trace files.')
gflags.DEFINE_integer('ignore_runs_before', 600000000,
                      'timestamp before which scheduler runs are ignored')
gflags.DEFINE_string('change_columns', '10,11,12,13,14',
                     'Column indices used to count changes.')

def get_algorithm_runtime_and_num_changes(trace_path, col_indices):
    # 10 nodes added
    # 11 nodes removed
    # 12 arcs added
    # 13 arcs changed
    # 14 arcs removed
    csv_file = open(trace_path + "/scheduler_events/scheduler_events.csv")
    csv_reader = csv.reader(csv_file)
    runtimes = []
    num_graph_changes = []
    for row in csv_reader:
        ts = long(row[0])
        if ts < FLAGS.ignore_runs_before:
            continue
        # XXX(ionel): HACK! There currently are only two outlier data points.
        # We do not include them in the graph because we do not have any
        # in-between points.
        if long(row[14]) + long(row[12]) > 100000:
            continue
        if long(row[2]) > 80000000:
            continue
        runtimes.append(long(row[2]))
        num_changes = 0
        for col_index in col_indices:
            num_changes = num_changes + long(row[col_index])
        num_graph_changes.append(num_changes)
    csv_file.close()
    return (runtimes, num_graph_changes)


def plot_scatter(plot_file_name, runtimes_vs_changes, labels, x_label, y_label):
    colors = ['r', 'b', 'g']
    markers = ['+', 'o', 'x']
    if FLAGS.paper_mode:
        plt.figure(figsize=(3.33, 2.22))
        set_paper_rcs()
    else:
        plt.figure()
        set_rcs()
    max_x = 0
    max_y = 0
    index = 0
    splts = []
    plt.xscale('log')
    for (runtimes, num_changes) in runtimes_vs_changes:
        max_x = max(max_x, np.max(num_changes))
        max_y = max(max_y, np.max(runtimes))
        if markers[index] == 'o':
            splt = plt.scatter(num_changes, [x / 1000 / 1000 for x in runtimes],
                               c=colors[index], marker=markers[index],
                               linewidth=0)
        else:
            splt = plt.scatter(num_changes, [x / 1000 / 1000 for x in runtimes],
                               c=colors[index], marker=markers[index])
        splts.append(splt)
        index = index + 1

    plt.xlim(0, max_x)
    plt.ylim(0, max_y / 1000 / 1000)
    plt.legend(splts, labels, scatterpoints=1, loc='upper left')
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    plt.savefig("%s.pdf" % plot_file_name,
                format="pdf", bbox_inches="tight")


def main(argv):
    try:
        argv = FLAGS(argv)
    except gflags.FlagsError as e:
        print('%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS))

    trace_paths = FLAGS.trace_paths.split(',')
    labels = FLAGS.trace_labels.split(',')
    col_indices = FLAGS.change_columns.split(',')
    runtimes_vs_changes = []
    for trace_path in trace_paths:
        runtimes_vs_changes.append(
            get_algorithm_runtime_and_num_changes(trace_path,
                                                  [long(x) for x in col_indices]))
    plot_scatter('algorithm_runtime_vs_num_changes', runtimes_vs_changes,
                 labels, 'Number graph changes', 'Runtime [sec]')


if __name__ == '__main__':
  main(sys.argv)
