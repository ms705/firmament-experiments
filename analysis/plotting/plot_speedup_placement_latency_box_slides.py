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


def get_placement_latencies(trace_path):
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

    latencies = []
    task_submit_time = {}
    tasks_scheduled = set([])
    tasks_submitted = set([])
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
            if event_type == SUBMIT_EVENT:
                tasks_submitted.add(task_id)
                task_submit_time[task_id] = timestamp
            elif event_type == SCHEDULE_EVENT:
                if task_id in task_submit_time:
                    submit_time = task_submit_time[task_id]
                    if submit_time != 0 and timestamp != submit_time and task_id not in tasks_scheduled:
                        tasks_scheduled.add(task_id)
                        # Add the event because it's not a migration.
                        latencies.append(timestamp - submit_time)
                else:
                    print ("Error: schedule event before submit event for task "
                           "(%s, %s)" % (row[2], row[3]))
#                    exit(1)
        csv_file.close()
    return latencies


def plot_placement_latencies(latencies, labels, colors, schedulers):
    if FLAGS.paper_mode:
        plt.figure(figsize=(3, 2))
        set_paper_rcs()
    else:
        plt.figure()
        set_rcs()
    indices = {'cost scaling' : 1, 'relax' : 2, 'firmament' : 3}
    ax = plt.gca()

    for algo, all_latencies_vals in latencies.items():
        print len(all_latencies_vals)
        bp = percentile_box_plot(ax, all_latencies_vals, color=colors[algo],
                                 index_base=indices[algo], index_step=3)
    ax.tick_params(length=2)
#    if 'Cost scaling (Quincy)' in schedulers:
    plt.plot(-1, -1, label='Cost scaling (Quincy)', color='b', lw=1.0)
#    if 'Relaxation' in schedulers:
    plt.plot(-1, -1, label='Relaxation', color='g', lw=1.0)
#    if 'Firmament' in schedulers:
    plt.plot(-1, -1, label='Firmament', color='r', lw=1.0)


    for i in range(3, 3 * len(labels), 3):
        plt.axvline(i + 0.5, ls='-', color='k')

    ax.legend(frameon=False, loc="upper center", ncol=6,
              bbox_to_anchor=(0.0, 1.04, 1.0, 0.1), handletextpad=0.2,
              handlelength=0.7, columnspacing=0.2)

    #plt.errorbar(range(1, len(setups) + 1), [np.mean(x) for x in runtimes],
    #             yerr=[np.std(x) for x in runtimes], marker="x")
    plt.xlim(0.5, 3 * len(labels) + 0.5)
    plt.ylim(ymin=0, ymax=50)
    plt.xticks([x * 3 + 2.25 for x in range(0, len(labels))], labels)
    plt.yticks(range(0, 60000001, 10000000), range(0, 61, 10))
    plt.ylabel("Task placement latency [sec]")
    plt.xlabel("Google trace speedup")
    plt.savefig("google_speedup_placement_latency_box_whiskers.pdf",
                format="pdf", bbox_inches="tight")


def main(argv):
    try:
        argv = FLAGS(argv)
    except gflags.FlagsError as e:
        print('%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS))
    trace_paths = FLAGS.trace_paths.split(',')
    speedups = [long(x) for x in FLAGS.speedups.split(',')]
    latencies = {}
    for trace_path in trace_paths:
        placement_latencies = get_placement_latencies(trace_path)
        if 'rapid' in trace_path:
            if 'firmament' in latencies:
                latencies['firmament'].append(placement_latencies)
            else:
                latencies['firmament'] = [placement_latencies]
        elif 'cost_scaling' in trace_path:
            if 'cost scaling' in latencies:
                latencies['cost scaling'].append(placement_latencies)
            else:
                latencies['cost scaling'] = [placement_latencies]
        elif 'relax' in trace_path:
            if 'relax' in latencies:
                latencies['relax'].append(placement_latencies)
            else:
                latencies['relax'] = [placement_latencies]
        else:
            print 'Error: Unexpected algorithm'
            exit(1)

    if FLAGS.paper_mode:
        plt.figure(figsize=(3.33, 2.22))
        set_paper_rcs()
    else:
        plt.figure()
        set_rcs()

    latencies_dict = {}
    labels = []
    colors = {}
    schedulers = set([])
    for speedup_index in range(0, len(speedups)):
        labels.append(str(speedups[speedup_index]) + 'x')
        for algo, speedup_latencies in latencies.items():
            if algo not in latencies_dict:
                latencies_dict[algo] = [speedup_latencies[speedup_index]]
            else:
                latencies_dict[algo].append(speedup_latencies[speedup_index])
            if algo == 'firmament':
                colors[algo] = 'r'
                schedulers.add('Firmament')
            elif algo == 'cost scaling':
                colors[algo] = 'b'
                schedulers.add('Cost scaling (Quincy)')
            elif algo == 'relax':
                colors[algo] = 'g'
                schedulers.add('Relaxation')
            else:
                print 'Error: unknown algorithm ', algo
    # plt.legend(loc='lower right', frameon=False, handlelength=1.5,
    #            handletextpad=0.1, numpoints=1)
    plot_placement_latencies(latencies_dict, labels, colors, schedulers)


if __name__ == '__main__':
  main(sys.argv)
