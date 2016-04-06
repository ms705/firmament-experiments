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
gflags.DEFINE_integer('time_interval', 100000000, 'Size of time interval in us')

MACHINE_REMOVED = 1
START_TIME = 600000000


def get_machine_removals_per_time_interval(trace_path):
    removals_per_interval = []
    csv_file = open(trace_path + "/machine_events/part-00000-of-00001.csv")
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        timestamp = long(row[0])
        if long(row[2]) == MACHINE_REMOVED:
            index = (timestamp - START_TIME) / FLAGS.time_interval
            while index >= len(removals_per_interval):
                removals_per_interval.append(0)
            removals_per_interval[index] += 1
    removals_per_interval.sort()
    return removals_per_interval


def plot_cdf(plot_file_name, cdf_vals, label_axis, labels, log_scale=False,
             bin_width=1000):
    colors = ['b', 'r', 'g', 'c', 'm', 'y', 'k']
    if FLAGS.paper_mode:
        plt.figure(figsize=(3.33, 2.22))
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
        plt.xticks(range(0, max_cdf_val, 1),
                   [str(x) for x in range(0, max_cdf_val, 1)])
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

    plot_cdf('machine_removals_per_time_interval_cdf',
             [get_machine_removals_per_time_interval(FLAGS.trace_path)],
             'Number machines removals events per time interval',
             ['100 second'], log_scale=False, bin_width=1)


if __name__ == '__main__':
  main(sys.argv)
