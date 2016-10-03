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
gflags.DEFINE_integer('num_files_to_process', 1,
                      'The number of trace files to process.')
gflags.DEFINE_bool('paper_mode', False, 'Adjusts the size of the plots.')
gflags.DEFINE_string('trace_paths', '',
                     ', separated list of path to trace files.')
gflags.DEFINE_string('trace_labels', '',
                     ', separated list of labels to use for trace files.')
gflags.DEFINE_integer('runtimes_after_timestamp', 0,
                      'Only plot runtimes of runs that happened after.')
gflags.DEFINE_integer('runtimes_before_timestamp', 0,
                      'Only plot runtimes that happened before.')


def get_scheduler_runtimes(trace_path, column_index):
    # 0 timestamp
    # 1 solver runtime
    # 2 algorithm runtime
    # 3 total runtime (including Firmament)
    runtimes = []
    timestamps = []
    csv_file = open(trace_path + "/scheduler_events/scheduler_events.csv")
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        timestamp = long(row[0])
        if timestamp > FLAGS.runtimes_after_timestamp and timestamp < FLAGS.runtimes_before_timestamp:
            timestamps.append(timestamp)
            runtimes.append(long(row[column_index]))
    csv_file.close()
    return (timestamps, runtimes)


def plot_timeline(plot_file_name, all_x_vals, all_y_vals, labels, unit='sec'):
    markers = {'Firmament':'x', 'Cost scaling (Quincy)':'o',
               'Relaxation only':'+', 'succ. shortest':'^'}
    colors = {'Firmament':'r', 'Cost scaling (Quincy)':'b',
              'Relaxation only':'g', 'succ. shortest':'c'}
    if FLAGS.paper_mode:
        plt.figure(figsize=(3, 2))
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
        if labels[index] != 'Relaxation only':
            plt.plot(all_x_vals[index], [x / 1000 / 1000 for x in all_y_vals[index]],
                     label=labels[index],
                     marker=markers[labels[index]],
                     color=colors[labels[index]],
                     mfc='none', mec=colors[labels[index]],
                     mew=1.0, lw=1.0, markevery=2)
        else:
            plt.plot(all_x_vals[index], [x / 1000 / 1000 for x in all_y_vals[index]],
                     label=labels[index],
                     marker=markers[labels[index]],
                     color=colors[labels[index]],
                     mfc='none', mec=colors[labels[index]],
                     mew=1.0, lw=1.0, markevery=1)
    max_y_val = 200000001
    max_x_val = 4000000001
    plt.ylabel('Algorithm runtime [sec]')
    plt.yticks(range(0, max_y_val / 1000 / 1000 + 1, 40),
               range(0, max_y_val / 1000 / 1000 + 1, 40))
    plt.ylim(0, max_y_val / 1000 / 1000 + 1)


    plt.axvspan(1425626250, 1762088834, lw=0, color='0.8')
    plt.axvspan(2139708317, 3076590575, lw=0, color='0.8')

    # plt.annotate('oversubscribed', xy=(0.6, 0.9), xycoords='axes fraction',
    #              xytext=(20, 0), textcoords='offset points',
    #              arrowprops=dict(arrowstyle="->"), ha='left')

    plt.xlim(FLAGS.runtimes_after_timestamp, max_x_val)
    plt.xticks(range(FLAGS.runtimes_after_timestamp, max_x_val, 500000000),
               [str(x / 1000 / 1000) for x in range(FLAGS.runtimes_after_timestamp, max_x_val, 500000000)])
    plt.xlabel('Simulation Time [' + unit + ']')
    plt.legend(loc='upper left', frameon=False, handlelength=1.0,
               handletextpad=0.2, numpoints=1)
    plt.savefig("%s.pdf" % plot_file_name,
                format="pdf", bbox_inches="tight")


def main(argv):
    try:
        argv = FLAGS(argv)
    except gflags.FlagsError as e:
      print('%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS))

    trace_paths = FLAGS.trace_paths.split(',')
    labels = FLAGS.trace_labels.split(',')
    all_timestamps = []
    all_runtimes = []
    for trace_path in trace_paths:
        (timestamps, runtimes) = get_scheduler_runtimes(trace_path, 2)
        all_timestamps.append(timestamps)
        all_runtimes.append(runtimes)

    plot_timeline('rapid_recovering_timeline', all_timestamps, all_runtimes,
                  labels, unit='sec')


if __name__ == '__main__':
  main(sys.argv)
