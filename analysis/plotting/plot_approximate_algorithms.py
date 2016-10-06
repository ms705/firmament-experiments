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
gflags.DEFINE_string('input_files', '', ', separated list of CSVs containing '
                     'the results.')
gflags.DEFINE_string('labels', '', ', separated list of labels')
gflags.DEFINE_bool('log_scale', False, 'Plot in log scale.')

def plot_timeline(plot_file_name, x_vals, y_vals, labels, log_scale):
    markers = {'cycle cancelling':'x', 'Cost scaling':'o', 'Relaxation':'+',
               'succ. shortest':'^'}
    colors = {'cycle cancelling':'r', 'Cost scaling':'b', 'Relaxation':'g',
              'succ. shortest':'c'}
    if FLAGS.paper_mode:
        plt.figure(figsize=(3, 2))
        set_paper_rcs()
    else:
        plt.figure()
        set_rcs()

    max_x_val = 0
    max_y_val = 0
    index = 0
    while index < len(x_vals):
        algo = labels[index]
        max_x_val = max(max_x_val, np.max(x_vals[index]))
        max_y_val = max(max_y_val, np.max(y_vals[index]))
        plt.plot([x / 1000 / 1000 for x in x_vals[index]], y_vals[index],
                 label=algo, color=colors[algo], marker=markers[algo],
                 mfc='none', mec=colors[algo], mew=1.0, lw=1.0, markevery=2)
        index = index + 1

    if log_scale:
        plt.yscale("log")
    else:
        plt.ylim(0, 5200)

    plt.xlim(0, max_x_val / 1000 / 1000)
    plt.xlabel('Algorithm runtime [sec]')
    # plt.xticks(range(0, 1000, 5001), ["%u" % x for x in range(0, 1000, 5001)],
    #            rotation=30, ha='right')
    plt.ylabel('Task misplacements')
    plt.legend(loc=1, frameon=False, handlelength=1.5, handletextpad=0.1,
               numpoints=1)
    plt.savefig("%s.pdf" % plot_file_name,
                format="pdf", bbox_inches="tight")


def main(argv):
    try:
        argv = FLAGS(argv)
    except gflags.FlagsError as e:
        print('%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS))

    input_files = FLAGS.input_files.split(',')
    labels = FLAGS.labels.split(',')
    all_timestamps = []
    all_misplacements = []
    for input_file in input_files:
        csv_file = open(input_file)
        csv_reader = csv.reader(csv_file)
        timestamps = []
        evictions = []
        migrations = []
        new_scheduled = []
        misplacements = []
        for row in csv_reader:
            timestamps.append(long(row[1]))
            evictions.append(long(row[2]))
            migrations.append(long(row[3]))
            new_scheduled.append(long(row[4]))
            misplacement = long(row[2]) + long(row[3])
            if misplacement == 0:
                misplacements.append(1)
            else:
                misplacements.append(misplacement)
        all_timestamps.append(timestamps)
        all_misplacements.append(misplacements)
        csv_file.close()

    plot_timeline('approximate_timeline', all_timestamps, all_misplacements,
                  labels, log_scale=FLAGS.log_scale)

if __name__ == '__main__':
  main(sys.argv)
