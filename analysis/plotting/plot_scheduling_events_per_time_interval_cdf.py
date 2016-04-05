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

def get_events_cnt_per_time_interval(trace_path, time_interval):
    events_per_interval = []
    for num_file in range(0, FLAGS.num_files_to_process, 1):
        csv_file = open(trace_path + "/task_events/part-" +
                        '{:05}'.format(num_file) + "-of-00500.csv")
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            timestamp = long(row[0])
            if FLAGS.ignore_time_zero_events is False or timestamp > START_TIME:
                index = (timestamp - START_TIME) / time_interval
                while index >= len(events_per_interval):
                    events_per_interval.append(0)
                events_per_interval[index] += 1
    return events_per_interval


def plot_cdf(plot_file_name, cdf_vals, label_axis, labels, log_scale=False,
             bin_width=1000):
    colors = ['b', 'r', 'g', 'c', 'm', 'y', 'k']
    if FLAGS.paper_mode:
        plt.figure(figsize=(2.33, 1.55))
        set_paper_rcs()
    else:
        plt.figure()
        set_rcs()

    max_cdf_val = 0
    max_perc90 = 0
    max_perc99 = 0
    index = 0
    for vals in cdf_vals:
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
        print "PERCENTILES:"
        perc1 = np.percentile(vals, 1)
        print "  1st: %f" % (perc1)
        perc10 = np.percentile(vals, 10)
        print " 10th: %f" % (perc10)
        perc25 = np.percentile(vals, 25)
        print " 25th: %f" % (perc25)
        perc50 = np.percentile(vals, 50)
        print " 50th: %f" % (perc50)
        perc75 = np.percentile(vals, 75)
        print " 75th: %f" % (perc75)
        perc90 = np.percentile(vals, 90)
        max_perc90 = max(max_perc90, perc90)
        print " 90th: %f" % (perc90)
        perc99 = np.percentile(vals, 99)
        max_perc99 = max(max_perc99, perc99)
        print " 99th: %f" % (perc99)

        bin_range = max_val - min_val
        num_bins = bin_range / bin_width
        (n, bins, patches) = plt.hist(vals, bins=num_bins, log=False,
                                      normed=True, cumulative=True,
                                      histtype="step", color=colors[index])
        # hack to add line to legend
        plt.plot([-100], [-100], label=labels[index],
                 color=colors[index], linestyle='solid', lw=1.0)
        # hack to remove vertical bar
        patches[0].set_xy(patches[0].get_xy()[:-1])

        index += 1


    if log_scale:
        plt.gca().set_xscale("log")
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

    time_intervals = FLAGS.time_intervals.split(',')
    labels = FLAGS.time_labels.split(',')
    time_interval_vals = []
    for time_interval in time_intervals:
        time_interval_vals.append(get_events_cnt_per_time_interval(
            FLAGS.trace_path, long(time_interval)))

    plot_cdf('scheduling_events_per_time_interval_cdf', time_interval_vals,
             'Number events per time interval', labels, log_scale=True,
             bin_width=1)


if __name__ == '__main__':
  main(sys.argv)