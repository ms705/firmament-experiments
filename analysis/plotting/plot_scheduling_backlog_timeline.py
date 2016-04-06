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
gflags.DEFINE_integer('runtimes_after_timestamp', 0,
                      'Only plot % unscheduled for runs that happened after.')


def get_percentage_unsched_tasks(trace_path):
    csv_file = open(trace_path + "/scheduler_events/scheduler_events.csv")
    csv_reader = csv.reader(csv_file)
    perc_unsched_tasks = []
    timestamps = []
    for row in csv_reader:
        timestamp = long(row[0])
        if timestamp <= FLAGS.runtimes_after_timestamp:
            continue

        timestamps.append(timestamp)
        perc_unsched_tasks.append(float(row[4]) / float(row[7]) * 100.0)
    csv_file.close()
    return (timestamps, perc_unsched_tasks)


def plot_timeline(plot_file_name, all_x_vals, all_y_vals, labels, unit='sec'):
    colors = ['b', 'r', 'g', 'c', 'm', 'y', 'k']
    if FLAGS.paper_mode:
        plt.figure(figsize=(3.33, 2.22))
        set_paper_rcs()
    else:
        plt.figure()
        set_rcs()
    index = 0
    max_x_val = 0
    max_y_val = 0
    for index in range(0, len(all_x_vals)):
        max_x_val = max(max_x_val, np.max(all_x_vals[index]))
        max_y_val = max(max_y_val, np.max(all_y_vals[index]))
        plt.plot(all_x_vals[index], all_y_vals[index], label=labels[index],
                 color=colors[index])
    plt.ylabel('\% unscheduled tasks')
    plt.ylim(0, max_y_val + 1)
    plt.xlim(0, max_x_val)

    if unit is 'ms':
        plt.xlim(0, max_x_val / 1000)
        plt.xticks(range(0, max_x_val, 1000000000),
                   [str(x / 1000) for x in range(0, max_x_val, 1000000000)])
    elif unit is 'sec':
        plt.xlim(0, max_x_val / 1000 / 1000)
        plt.xticks(range(0, max_x_val, 1000000000),
                   [str(x / 1000 / 1000) for x in range(0, max_x_val, 1000000000)])
    else:
        print 'Error: unknown time unit'
        exit(1)
    plt.xlabel('Time [' + unit + ']')
    plt.legend(loc=4, frameon=False, handlelength=2.5, handletextpad=0.2)
    plt.savefig("%s.pdf" % plot_file_name,
                format="pdf", bbox_inches="tight")


def main(argv):
    try:
        argv = FLAGS(argv)
    except gflags.FlagsError as e:
      print('%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS))
    trace_paths = FLAGS.trace_paths.split(',')
    labels = FLAGS.trace_labels.split(',')
    perc_unsched_tasks = []
    all_timestamps = []
    for trace_path in trace_paths:
        (timestamps, unsched) = get_percentage_unsched_tasks(trace_path)
        all_timestamps.append(timestamps)
        perc_unsched_tasks.append(unsched)

    plot_timeline('percentage_unscheduled_tasks_timeline', all_timestamps,
                  perc_unsched_tasks, labels, unit='sec')


if __name__ == '__main__':
  main(sys.argv)
