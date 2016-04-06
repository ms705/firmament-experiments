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
gflags.DEFINE_bool('ignore_time_zero_events', True,
                   'True if the plot should ignore the events from the '
                   'beginning of the trace.')
gflags.DEFINE_string('trace_path', '', 'Path to the trace')
gflags.DEFINE_string('time_intervals', '1000000',
                     ', separated sizes of time interval in us')
gflags.DEFINE_string('time_labels', '1000 ms', ', separated list of labels')

START_TIME = 600000000

TASK_SUBMIT_EVENT = 0
TASK_SCHEDULE_EVENT = 1
TASK_EVICT_EVENT = 2
TASK_FAIL_EVENT = 3
TASK_FINISH_EVENT = 4
TASK_KILL_EVENT = 5
TASK_LOST_EVENT = 6

def get_events_cnt_per_time_interval(trace_path, time_interval):
    events_per_interval = []
    for num_file in range(0, FLAGS.num_files_to_process, 1):
        csv_file = open(trace_path + "/task_events/part-" +
                        '{:05}'.format(num_file) + "-of-00500.csv")
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            timestamp = long(row[0])
            event_type = long(row[3])
            # Ignore the schedule events because they're scheduling policy
            # specific.
            if event_type == TASK_SCHEDULE_EVENT:
                continue
            # XXX(ionel): Hack to ignore the events beyond 30 days.
            if timestamp > 2592000000000:
                continue
            if FLAGS.ignore_time_zero_events is False or timestamp > START_TIME:
                index = (timestamp - START_TIME) / time_interval
                while index >= len(events_per_interval):
                    events_per_interval.append(0)
                events_per_interval[index] += 1
        csv_file.close()
    return events_per_interval


def plot_cdf(plot_file_name, label_axis, labels, log_scale=False,
             bin_width=1000):
    colors = ['b', 'r', 'g', 'c', 'm', 'y', 'k', '0.2', '0.4', '0.6']
    if FLAGS.paper_mode:
        plt.figure(figsize=(3.33, 2.22))
        set_paper_rcs()
    else:
        plt.figure()
        set_rcs()

    max_cdf_val = 0
    index = 0
    time_intervals = FLAGS.time_intervals.split(',')
    for time_interval in time_intervals:
        vals = get_events_cnt_per_time_interval(FLAGS.trace_path,
                                                long(time_interval))
        print "Got %d values" % (len(vals))
        print "Statistics for %s" % (labels[index])
        avg = np.mean(vals)
        print "AVG: %f" % (avg)
        median = np.median(vals)
        print "MEDIAN: %f" % (median)
        min_val = np.min(vals)
        print "MIN: %ld" % (min_val)
        max_val = np.max(vals)
        max_cdf_val = max(max_val, max_cdf_val)
        print "MAX: %ld" % (max_val)
        stddev = np.std(vals)
        print "STDDEV: %f" % (stddev)

        bin_range = max_val - min_val
        num_bins = bin_range / bin_width

        hist, bin_edges = np.histogram(vals, bins=num_bins, normed=True)
        cdf = np.cumsum(hist)

        #(n, bins, patches) = plt.hist(vals, bins=num_bins, log=False,
        #                              normed=True, cumulative=True,
        #                              histtype="step", color=colors[index])
        # hack to add line to legend
        plt.plot(bin_edges[:-1], cdf, label=labels[index],
                 color=colors[index], linestyle='solid', lw=1.0)
        # hack to remove vertical bar
        #patches[0].set_xy(patches[0].get_xy()[:-1])

        index += 1
        del vals


    if log_scale:
        plt.xscale("log")
        plt.xlim(0, max_cdf_val)
        x_val = 1
        x_ticks = []
        while x_val <= max_cdf_val:
            x_ticks.append(x_val)
            x_val *= 10
        plt.xticks(x_ticks, [str(x) for x in x_ticks])
    else:
        plt.xlim(0, max_cdf_val)
        plt.xticks(range(0, max_cdf_val, 1000),
                   [str(x) for x in range(0, max_cdf_val, 1000)])
    plt.ylim(0, 1.0)
    plt.yticks(np.arange(0.0, 1.01, 0.2),
               [str(x) for x in np.arange(0.0, 1.01, 0.2)])

    plt.xlabel(label_axis)

    plt.legend(loc=4, frameon=False, handlelength=2.5, handletextpad=0.2)

    plt.savefig("%s.pdf" % plot_file_name,
                format="pdf", bbox_inches="tight")


def main(argv):
    try:
        argv = FLAGS(argv)
    except gflags.FlagsError as e:
        print('%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS))

    labels = FLAGS.time_labels.split(',')

    plot_cdf('scheduling_events_per_time_interval_cdf',
             'Task events per time interval', labels, log_scale=True,
             bin_width=1)


if __name__ == '__main__':
  main(sys.argv)
