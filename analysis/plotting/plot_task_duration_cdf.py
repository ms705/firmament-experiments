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

SUBMIT_EVENT = 0
SCHEDULE_EVENT = 1
EVICT_EVENT = 2
FINISH_EVENT = 4

def get_scheduling_delays(trace_path):
    delays = []
    task_submit_time = {}
    tasks_submitted = set([])
    task_scheduled = {}
    tasks_on_machine = {}
    for num_file in range(0, FLAGS.num_files_to_process, 1):
        csv_file = open(trace_path + "/task_events/part-" +
                        '{:05}'.format(num_file) + "-of-00500.csv")
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            timestamp = long(row[0])
            task_id = (long(row[2]), long(row[3]))
            machine = row[4]
            event_type = int(row[5])
            if event_type == SUBMIT_EVENT:
                tasks_submitted.add(task_id)
                task_submit_time[task_id] = timestamp
            elif event_type == SCHEDULE_EVENT:
                task_scheduled[task_id] = machine
                if machine in tasks_on_machine:
                    tasks_on_machine[machine] = tasks_on_machine[machine] + 1
                else:
                    tasks_on_machine[machine] = 1
                if tasks_on_machine[machine] > 2:
                    print "MACHINE", machine, "has", tasks_on_machine[machine]
            elif event_type == FINISH_EVENT:
                machine = task_scheduled[task_id]
                tasks_on_machine[machine] = tasks_on_machine[machine] - 1
                if task_id in task_submit_time:
                    submit_time = task_submit_time[task_id]
                    delays.append(timestamp - submit_time)
                    if timestamp - submit_time > 30000000:
                        print task_id
                else:
                    print ("Error: schedule event before submit event for task "
                           "(%s, %s)" % (row[2], row[3]))
                    exit(1)
        csv_file.close()
    print trace_path, 'tasks submitted:', len(tasks_submitted)
    return delays


def plot_cdf(plot_file_name, cdf_vals, label_axis, labels, log_scale=False,
             bin_width=1000, unit='ms'):
    colors = ['k', 'r', 'g', 'c', 'm', 'y', 'k']
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

    time_val = 1000
    if unit is 'ms':
        time_val = 1000 # 1 ms
    elif unit is 'sec':
        time_val = 1000 * 1000 # 1 sec
    else:
        print 'Error: unknown time unit'
        exit(1)
    max_cdf_val = 65000001
    if log_scale:
        plt.xscale("log")
        plt.xlim(0, max_cdf_val)
        to_time_unit = time_val
        x_ticks = []
        while time_val <= max_cdf_val:
            x_ticks.append(time_val)
            time_val *= 10
        plt.xticks(x_ticks, [str(x / to_time_unit) for x in x_ticks])
    else:
        plt.xlim(0, max_cdf_val)
        plt.xticks(range(0, max_cdf_val, 5000000),
                   [str(x / time_val) for x in range(0, max_cdf_val, 5000000)])
    plt.ylim(0, 1.0)
    plt.yticks(np.arange(0.0, 1.01, 0.2),
               [str(x) for x in np.arange(0.0, 1.01, 0.2)])
    plt.ylabel('CDF of task response time')
    plt.xlabel(label_axis)

    plt.legend(loc=4, frameon=False, handlelength=2.5, handletextpad=0.2)

    plt.savefig("%s.pdf" % plot_file_name,
                format="pdf", bbox_inches="tight")

    plt.ylim(0, 0.99)
    plt.xlim(0, max_perc99);
    plt.savefig("%s-99th.pdf" % plot_file_name,
                format="pdf", bbox_inches="tight")

    plt.ylim(0, 0.9)
    plt.xlim(0, max_perc90);
    plt.savefig("%s-90th.pdf" % plot_file_name,
                format="pdf", bbox_inches="tight")


def main(argv):
    try:
        argv = FLAGS(argv)
    except gflags.FlagsError as e:
        print('%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS))

    trace_paths = FLAGS.trace_paths.split(',')
    labels = FLAGS.trace_labels.split(',')
    delays = []
    for trace_path in trace_paths:
        trace_delays = get_scheduling_delays(trace_path)
        delays.append(trace_delays)

    plot_cdf('scheduling_delay_cdf', delays, "Task response time [sec]",
             labels, log_scale=False, bin_width=10000, unit='sec')


if __name__ == '__main__':
  main(sys.argv)
