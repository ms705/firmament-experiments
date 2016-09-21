# Copyright (c) 2016, Ionel Gog

import csv
import gflags
import math
import matplotlib
matplotlib.use("agg")
import os, sys
import matplotlib.pyplot as plt
import numpy as np
from utils import *
from process_synthetic_experiments import *
from matplotlib import pylab
from scipy.stats import scoreatpercentile
from box_and_whisker import *


FLAGS = gflags.FLAGS
gflags.DEFINE_integer('num_files_to_process', 1,
                      'The number of trace files to process.')
gflags.DEFINE_bool('paper_mode', False, 'Adjusts the size of the plots.')
gflags.DEFINE_integer('runtimes_after_timestamp', 0,
                      'Only plot runtimes of runs that happened after.')
gflags.DEFINE_string('trace_paths', '',
                     ', separated list of path to trace files.')
gflags.DEFINE_string('speedups', '',
                     ', separated list of labels to use for trace files.')
gflags.DEFINE_integer('runtime', 86400000000, 'Runtime of the simulation.')

SUBMIT_EVENT = 0
SCHEDULE_EVENT = 1
EVICT_EVENT = 2


def get_scheduling_delays(trace_path):
    print 'Reading ', trace_path
    runtime_factor = 1
    found_factor = False
    if 'x_speedup' in trace_path:
        elements = trace_path.split('_')
        for i in range(0, len(elements)):
            if elements[i] == 'speedup' and i > 0:
                found_factor = True
                runtime_factor = int(elements[i - 1][:-1])

    if 'speedup' in trace_path and not found_factor:
        print 'Error processing', trace_path
        exit(1)

    csv_file = open(trace_path + "/scheduler_events/scheduler_events.csv")
    csv_reader = csv.reader(csv_file)
    timestamps = []
    runtimes = []
    for row in csv_reader:
        timestamp = long(row[0])
        if timestamp > FLAGS.runtimes_after_timestamp / runtime_factor:
            timestamps.append(long(row[0]))
            runtimes.append(long(row[2]))
    csv_file.close()

    timestamp_len = len(timestamps)
    timestamp_index = 0
    # If a task is evicted and scheduled again then we will have
    # two or more scheduling delays for it.
    delays = []
    seen_last_scheduler_run = False

    scheduled_tasks = set([])
    for num_file in range(0, FLAGS.num_files_to_process, 1):
        csv_file = open(trace_path + "/task_events/part-" +
                        '{:05}'.format(num_file) + "-of-00500.csv")
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            timestamp = long(row[0])
            task_id = (long(row[2]), long(row[3]))
            event_type = int(row[5])
            if timestamp > FLAGS.runtime / runtime_factor:
                break
            if timestamp <= FLAGS.runtimes_after_timestamp / runtime_factor:
                continue
            if event_type == SCHEDULE_EVENT:
                scheduled_tasks.add(task_id)
        csv_file.close()

    for num_file in range(0, FLAGS.num_files_to_process, 1):
        csv_file = open(trace_path + "/task_events/part-" +
                        '{:05}'.format(num_file) + "-of-00500.csv")
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            timestamp = long(row[0])
            task_id = (long(row[2]), long(row[3]))
            event_type = int(row[5])
            if timestamp > FLAGS.runtime / runtime_factor:
                break
            if timestamp <= FLAGS.runtimes_after_timestamp / runtime_factor:
                continue

            while not seen_last_scheduler_run and timestamps[timestamp_index] < timestamp:
                timestamp_index = timestamp_index + 1
                if timestamp_index >= timestamp_len or timestamps[timestamp_index] * runtime_factor > FLAGS.runtime:
                    seen_last_scheduler_run = True
                    break

            if event_type == SUBMIT_EVENT:
                if seen_last_scheduler_run:
#                    delays.append()
                    my_index = 0
                else:
                    if task_id in scheduled_tasks:
                        delays.append(timestamps[timestamp_index] - timestamp +
                                      runtimes[timestamp_index])
                    else:
                        if timestamp_index + 1 < timestamp_len and timestamps[timestamp_index + 1] * runtime_factor < FLAGS.runtime:
                            delays.append(1000000000)

        csv_file.close()
    return delays


def plot_scheduling_delays(delays, labels, colors):
    if FLAGS.paper_mode:
        plt.figure(figsize=(3, 2))
        set_paper_rcs()
    else:
        plt.figure()
        set_rcs()

    ax = plt.gca()
    bp = percentile_box_plot(ax, delays, color=colors)

    plt.plot(-1, -1, label='Firmament', color='r', lw=1.0)
    plt.plot(-1, -1, label='Relaxation', color='g', lw=1.0)
#    plt.plot(-1, -1, label='Cost scaling', color='b', lw=1.0)

    for i in range(2, len(delays), 2):
        plt.axvline(i + 0.5, ls='-', color='k')

    ax.legend(frameon=False, loc="upper center", ncol=6,
              bbox_to_anchor=(0.0, 1.02, 1.0, 0.1), handletextpad=0.2,
              columnspacing=0.2)

    #plt.errorbar(range(1, len(setups) + 1), [np.mean(x) for x in runtimes],
    #             yerr=[np.std(x) for x in runtimes], marker="x")
    plt.xlim(0.5, len(delays) + 0.5)
    plt.ylim(ymin=0, ymax=30)
    plt.xticks([x * 2 + 1.5 for x in range(0, len(labels))], labels)
    plt.yticks(range(0, 20000001, 3000000), range(0, 21, 3))
    plt.ylabel("Task placement latency [sec]")
    plt.xlabel("Google trace speedup")
    plt.savefig("google_speedup_scheduling_delay_box_whiskers.pdf",
                format="pdf", bbox_inches="tight")


def main(argv):
    try:
        argv = FLAGS(argv)
    except gflags.FlagsError as e:
        print('%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS))
    trace_paths = FLAGS.trace_paths.split(',')
    speedups = [long(x) for x in FLAGS.speedups.split(',')]
    delays = {}
    for trace_path in trace_paths:
        trace_delays = get_scheduling_delays(trace_path)
        if 'rapid' in trace_path:
            if 'Firmament' in delays:
                delays['Firmament'].append(trace_delays)
            else:
                delays['Firmament'] = [trace_delays]
        elif 'cost_scaling' in trace_path:
            if 'cost scaling' in delays:
                delays['cost scaling'].append(trace_delays)
            else:
                delays['cost scaling'] = [trace_delays]
        elif 'relax' in trace_path:
            if 'relax' in delays:
                delays['relax'].append(trace_delays)
            else:
                delays['relax'] = [trace_delays]
        else:
            print 'Error: Unexpected algorithm'
            exit(1)

    if FLAGS.paper_mode:
        plt.figure(figsize=(3.33, 2.22))
        set_paper_rcs()
    else:
        plt.figure()
        set_rcs()

    delay_list = []
    labels = []
    colors = ['k']
    for speedup_index in range(0, len(speedups)):
        labels.append(str(speedups[speedup_index]) + 'x')
        for algo, speedup_delays in delays.items():
            delay_list.append(speedup_delays[speedup_index])
            if algo == 'Firmament':
                colors.append('r')
            elif algo == 'cost scaling':
                colors.append('b')
            elif algo == 'relax':
                colors.append('g')
            else:
                print 'Error: unknown algorithm ', algo
    print len(delay_list)
    print labels
    print colors
    # plt.legend(loc='lower right', frameon=False, handlelength=1.5,
    #            handletextpad=0.1, numpoints=1)
    plot_scheduling_delays(delay_list, labels, colors)


if __name__ == '__main__':
  main(sys.argv)
