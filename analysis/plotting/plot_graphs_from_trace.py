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
gflags.DEFINE_bool('plot_scheduling_delay_cdf', False,
                   'Plot CDF of scheduling delay.')
gflags.DEFINE_bool('ignore_delay_first_solver_run', True,
                   'True if the plot should not include the scheduling delay '
                   'of the tasks scheduled in the first solver run.')
gflags.DEFINE_bool('plot_solver_runtime_cdf', False,
                   'Plot CDF of solver runtimes.')
gflags.DEFINE_bool('plot_solver_runtime_timeline', False,
                   'Print timeline of solver runtimes.')
gflags.DEFINE_bool('plot_algorithm_runtime_vs_num_changes', False,
                   'Plot algorithm runtime vs number changes.')
gflags.DEFINE_string('trace_path', '', 'Path to where the trace files.')

SUBMIT_EVENT = 0
SCHEDULE_EVENT = 1
EVICT_EVENT = 2


def plot_cdf(plot_file_name, cdf_vals, label_axis, labels, log_scale=False,
             bin_width=1000, unit='ms'):
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
        time_val = 1000
        if unit is 'ms':
            time_val = 1000 # 1 ms
        elif unit is 'sec':
            time_val = 1000 * 1000 # 1 sec
        else:
            print 'Error: unknown time unit'
            exit(1)
        to_time_unit = time_val
        x_ticks = []
        while time_val <= max_cdf_val:
            x_ticks.append(time_val)
            time_val *= 10
        plt.xticks(x_ticks, [str(x / to_time_unit) for x in x_ticks])
    else:
        plt.xlim(0, max_cdf_val)
        plt.xticks(range(0, max_cdf_val, 1000000),
                   [str(x / 1000) for x in range(0, max_cdf_val, 1000000)])
    plt.ylim(0, 1.0)
    plt.yticks(np.arange(0.0, 1.01, 0.2),
               [str(x) for x in np.arange(0.0, 1.01, 0.2)])

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


# def plot_barchart(plot_file_name, bar_vals, label_axis, labels):
#     colors = ['b', 'r', 'g', 'c', 'm', 'y', 'k']
#     if FLAGS.paper_mode:
#         plt.figure(figsize=(3.0, 2.0))
#         set_paper_rcs()
#     else:
#         plt.figure()
#         set_rcs()

#     bar_width = 0.09
#     bar_gap = 0.01

#     bar_index = 0
#     for vals in bar_vals:
#         plt.barh(bar_index * (width + gap), vals, color=colors[bar_index],
#                  lw=0.5, label=labels[bar_index])


def plot_scatter(plot_file_name, x_vals, y_vals, x_label, y_label):
    if FLAGS.paper_mode:
        plt.figure(figsize=(2.33, 1.55))
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


def get_scheduling_delays(trace_path):
    # If a task is evicted and scheduled again then we will have
    # two or more scheduling delays for it.
    delays = []
    task_submit_time = {}
    for num_file in range(0, FLAGS.num_files_to_process, 1):
        csv_file = open(trace_path + "task_events/part-" +
                        '{:05}'.format(num_file) + "-of-00500.csv")
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            timestamp = long(row[0])
            task_id = (long(row[2]), long(row[3]))
            event_type = int(row[5])
            if event_type == SUBMIT_EVENT:
                task_submit_time[task_id] = timestamp
            elif event_type == SCHEDULE_EVENT:
                if task_id in task_submit_time:
                    submit_time = task_submit_time[task_id]
                    if (submit_time != 0 or
                        FLAGS.ignore_delay_first_solver_run is False):
                        delays.append(timestamp - submit_time)
                    del task_submit_time[task_id]
                else:
                    print ("Error: schedule event before submit event for task "
                           "(%s, %s)" % (row[2], row[3]))
                    exit(1)
        csv_file.close()
    delays.sort()
    return delays


def get_scheduler_runtimes(trace_path, column_index):
    # 0 timestamp
    # 1 solver runtime
    # 2 algorithm runtime
    # 3 total runtime (including Firmament)
    runtimes = []
    csv_file = open(trace_path + "scheduler_events/scheduler_events.csv")
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        runtimes.append(long(row[column_index]))
    csv_file.close()
    runtimes.sort()
    return runtimes


def get_algorithm_runtime_and_num_changes(trace_path):
    # 4 nodes added
    # 5 nodes removed
    # 6 arcs added
    # 7 arcs changed
    # 8 arcs removed
    csv_file = open(trace_path + "scheduler_events/scheduler_events.csv")
    csv_reader = csv.reader(csv_file)
    runtimes = []
    num_graph_changes = []
    for row in csv_reader:
        runtimes.append(long(row[2]))
        num_graph_changes.append(long(row[4]) + long(row[5]) + long(row[6]) +
                                 long(row[6]) + long(row[7]) + long(row[8]))
    csv_file.close()
    return (runtimes, num_graph_changes)


def main(argv):
    try:
        argv = FLAGS(argv)
    except gflags.FlagsError as e:
      print('%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS))

    if FLAGS.plot_scheduling_delay_cdf:
        delays = get_scheduling_delays(FLAGS.trace_path)
        print "Number tasks scheduled: %d" % (len(delays))
        plot_cdf('scheduling_delay_cdf.pdf', [delays], "Latency [sec]",
                 ["Google"], log_scale=True, bin_width=1000000, unit='sec')

    if FLAGS.plot_solver_runtime_cdf:
        scheduler_runtimes = get_scheduler_runtimes(FLAGS.trace_path, 1)
        algorithm_runtimes = get_scheduler_runtimes(FLAGS.trace_path, 2)
        print "Number scheduler runs: %d" % (len(scheduler_runtimes))
        plot_cdf('scheduling_runtimes_cdf.pdf',
                 [scheduler_runtimes, algorithm_runtimes],
                 "Latency [ms]", ["Scheduler", "Algorithm"],
                 log_scale=True, bin_width=1000, unit='ms')

    if FLAGS.plot_solver_runtime_timeline:
        print 'Error: not implemented'
        exit(1)

    if FLAGS.plot_algorithm_runtime_vs_num_changes:
        (runtimes, num_graph_changes) = get_algorithm_runtime_and_num_changes(FLAGS.trace_path)
        print "Number scheduler runs: %d" % (len(runtimes))
        plot_scatter('algorithm_runtime_vs_num_changes.pdf',
                     [x / 1000 for x in runtimes], num_graph_changes,
                     'Runtime [ms]', 'Number graph changes')


if __name__ == '__main__':
  main(sys.argv)
