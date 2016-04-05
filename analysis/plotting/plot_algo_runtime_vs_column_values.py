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
gflags.DEFINE_bool('ignore_first_run', True,
                   'True if the first run should be ignored')
gflags.DEFINE_integer('column_index', 0, 'The column index in the '
                      'scheduler_events table to plot runtime against')
gflags.DEFINE_string('label', '', 'The label of the column')


def get_algorithm_runtime_and_column(trace_path, column_index):
    csv_file = open(trace_path + "/scheduler_events/scheduler_events.csv")
    csv_reader = csv.reader(csv_file)
    runtimes = []
    num_graph_changes = []
    for row in csv_reader:
        runtimes.append(long(row[2]))
        num_graph_changes.append(long(row[column_index]))
    csv_file.close()
    return (runtimes[1:], num_graph_changes[1:])


def plot_scatter(plot_file_name, x_vals, y_vals, x_label, y_label):
    if FLAGS.paper_mode:
        plt.figure(figsize=(3.33, 2.22))
        set_paper_rcs()
    else:
        plt.figure()
        set_rcs()

    plt.scatter(x_vals, y_vals)
    plt.xlim(0, np.max(x_vals))
    plt.ylim(0, np.max(y_vals))
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

    if len(trace_paths) != 1:
        print 'Error: cannot plot for more than a trace'
        exit(1)

    (runtimes, col_vals) = get_algorithm_runtime_and_column(trace_paths[0],
                                                            FLAGS.column_index)
    print "Number scheduler runs: %d" % (len(runtimes))
    plot_scatter('algorithm_runime_vs_column',
                 [x / 1000 for x in runtimes], col_vals,
                 'Runtime [ms]', FLAGS.label)


if __name__ == '__main__':
  main(sys.argv)
