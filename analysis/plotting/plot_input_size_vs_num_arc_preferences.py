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
gflags.DEFINE_string('trace_path', '', 'Path to the trace')

BYTES_TO_MB = 1048576
BYTES_TO_GB = 1073741824
BLOCK_ADD = 0
BLOCK_REMOVE = 1


def get_input_and_num_arc_preferences(trace_path):
    csv_file = open(trace_path + "/quincy_tasks/quincy_tasks.csv")
    csv_reader = csv.reader(csv_file)
    input_sizes = []
    num_preferences = []
    for row in csv_reader:
        input_sizes.append(long(row[3]))
        num_preferences.append(long(row[8]) + long(row[9]))
    csv_file.close()
    return (input_sizes, num_preferences)


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

    (input_sizes, num_preferences) = get_input_and_num_arc_preferences(FLAGS.trace_path)

    plot_scatter('input_size_vs_num_arc_preferences',
                 [x / BYTES_TO_GB for x in input_sizes], num_preferences,
                 'Task input size [GB]', 'Number rack or machine preferences')


if __name__ == '__main__':
  main(sys.argv)
