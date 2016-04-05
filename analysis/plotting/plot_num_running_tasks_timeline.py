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
gflags.DEFINE_string('trace_path', '', 'Path to the trace')
gflags.DEFINE_integer('time_interval', 1000000, 'Size of time interval in us')

SCHEDULE_EVENT = 1
EVICT_EVENT = 2
FAIL_EVENT = 3
FINISH_EVENT = 4
KILL_EVENT = 5
LOST_EVENT = 6


def get_num_running_tasks_per_time_interval(trace_path):
    num_running_per_interval = []
    timestamps = []
    cur_num_running = 0
    for num_file in range(0, FLAGS.num_files_to_process, 1):
        csv_file = open(trace_path + "/task_events/part-" +
                        '{:05}'.format(num_file) + "-of-00500.csv")
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            timestamp = long(row[0])
            event_type = int(row[5])
            index = timestamp / FLAGS.time_interval
            while index >= len(num_running_per_interval):
                num_running_per_interval.append(cur_num_running)
                timestamps.append(index * FLAGS.time_interval)
            if event_type == SCHEDULE_EVENT:
                cur_num_running += 1
            elif (event_type == EVICT_EVENT or event_type == KILL_EVENT or
                  event_type == FAIL_EVENT or event_type == FINISH_EVENT or
                  event_type == LOST_EVENT):
                cur_num_running -= 1
            num_running_per_interval[index] = cur_num_running
        csv_file.close()
    return (timestamps, num_running_per_interval)


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
        print 'Maximum number of running tasks: %d' % (max_y_val)
        plt.plot(all_x_vals[index], all_y_vals[index],
                 label=labels[index], linestyle='none', marker='x',
                 color=colors[index])
    plt.ylabel('Number running tasks')
    plt.ylim(0, max_y_val + 1)

    if unit is 'ms':
        plt.xlim(0, max_x_val)
        plt.xticks(range(0, max_x_val, 1000000000),
                   [str(x / 1000) for x in range(0, max_x_val, 1000000000)])
    elif unit is 'sec':
        plt.xlim(0, max_x_val)
        plt.xticks(range(0, max_x_val, 1000000000),
                   [str(x / 1000 / 1000) for x in range(0, max_x_val, 1000000000)])
    else:
        print 'Error: unknown time unit'
        exit(1)
    plt.xlabel('Time [' + unit + ']')
    plt.legend(loc=1, frameon=False, handlelength=2.5, handletextpad=0.2)
    plt.savefig("%s.pdf" % plot_file_name,
                format="pdf", bbox_inches="tight")


def main(argv):
    try:
        argv = FLAGS(argv)
    except gflags.FlagsError as e:
      print('%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS))

    (timestamps, num_running_tasks) = get_num_running_tasks_per_time_interval(FLAGS.trace_path)
    plot_timeline('num_running_tasks_timeline', [timestamps],
                  [num_running_tasks], ['Google'], unit='sec')


if __name__ == '__main__':
  main(sys.argv)
