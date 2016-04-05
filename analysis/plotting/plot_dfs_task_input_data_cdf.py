# Copyright (c) 2016, Ionel Gog

import csv
import gflags
import math
import matplotlib
matplotlib.use("agg")
import os, sys
import matplotlib.pyplot as plt
from collections import defaultdict
from utils import *

FLAGS = gflags.FLAGS
gflags.DEFINE_bool('paper_mode', False, 'Adjusts the size of the plots.')
gflags.DEFINE_string('trace_path', '', 'Path to the trace')

BYTES_TO_MB = 1048576
BYTES_TO_GB = 1073741824
BLOCK_ADD = 0
BLOCK_REMOVE = 1

def get_input_data_per_task(trace_path):
    csv_file = open(trace_path + "/tasks_to_blocks/tasks_to_blocks.csv")
    csv_reader = csv.reader(csv_file)
    block_jobs = defaultdict(list)
    for row in csv_reader:
        job_id = long(row[0])
        task_index = long(row[1])
        block_id = long(row[2])
        block_jobs[block_id].append((job_id, task_index))
    csv_file.close()

    csv_file = open(trace_path + "/dfs_events/dfs_events.csv")
    csv_reader = csv.reader(csv_file)
    task_input = {}
    for row in csv_reader:
        event_type = int(row[1])
        block_id = long(row[3])
        block_size = 0
        if event_type == BLOCK_ADD:
            block_size = long(row[4])
        elif event_type == BLOCK_REMOVE:
            block_size = -long(row[4])
        else:
            print 'ERROR: unexpected event type'
        for task_id in block_jobs[block_id]:
            if task_id in task_input:
                task_input[task_id] = task_input[task_id] + block_size
            else:
                task_input[task_id] = block_size
    csv_file.close()
    return task_input.values()


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
    index = 0
    for vals in cdf_vals:
#        print "Statistics for %s" % (labels[index])
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
        print " 90th: %f" % (perc90)
        perc99 = np.percentile(vals, 99)
        print " 99th: %f" % (perc99)

        bin_range = max_val - min_val + 1
        num_bins = bin_range / bin_width
        (n, bins, patches) = plt.hist(vals, bins=num_bins, log=False,
                                      normed=True, cumulative=True,
                                      histtype="step", color=colors[index])
        # hack to add line to legend
        # plt.plot([-100], [-100], label=labels[index],
        #          color=colors[index], linestyle='solid', lw=1.0)
        # hack to remove vertical bar
        patches[0].set_xy(patches[0].get_xy()[:-1])

        index += 1

    if log_scale:
        plt.xscale("log")
        plt.xlim(0, max_cdf_val)
        # Start at 1GB.
        x_val = BYTES_TO_GB
        x_ticks = []
        while x_val <= max_cdf_val:
            x_ticks.append(x_val)
            x_val *= 10
        plt.xticks(x_ticks, [str(x / BYTES_TO_GB) for x in x_ticks])
    else:
        plt.xlim(0, max_cdf_val)
        plt.xticks(range(0, max_cdf_val, 5 * BYTES_TO_GB),
                   [str(x / BYTES_TO_GB) for x in range(0, max_cdf_val, 5 * BYTES_TO_GB)])
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

    plot_cdf('dfs_task_input_data_cdf',
             [get_input_data_per_task(FLAGS.trace_path)],
             'Input data per task [GB]', [], log_scale=False, bin_width=BYTES_TO_MB)


if __name__ == '__main__':
  main(sys.argv)
