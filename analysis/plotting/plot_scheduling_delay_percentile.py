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
    csv_file = open(trace_path + "/scheduler_events/scheduler_events.csv")
    csv_reader = csv.reader(csv_file)
    timestamps = []
    runtimes = []
    for row in csv_reader:
        timestamp = long(row[0])
        if timestamp > FLAGS.runtimes_after_timestamp:
            timestamps.append(long(row[0]))
            runtimes.append(long(row[2]))
    csv_file.close()

    runtime_factor = 1
    if '2x_speedup' in trace_path:
        runtime_factor = 2
    elif '3x_speedup' in trace_path:
        runtime_factor = 3
    elif '4x_speedup' in trace_path:
        runtime_factor = 4
    elif '5x_speedup' in trace_path:
        runtime_factor = 5
    elif '6x_speedup' in trace_path:
        runtime_factor = 6
    elif '7x_speedup' in trace_path:
        runtime_factor = 7
    elif '8x_speedup' in trace_path:
        runtime_factor = 8
    elif '9x_speedup' in trace_path:
        runtime_factor = 9
    elif '10x_speedup' in trace_path:
        runtime_factor = 10

    elif 'speedup' in trace_path:
        print 'Error processing', trace_path
        exit(1)

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
            if timestamp <= FLAGS.runtimes_after_timestamp:
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
            if timestamp <= FLAGS.runtimes_after_timestamp:
                continue

            while not seen_last_scheduler_run and timestamps[timestamp_index] < timestamp:
                timestamp_index = timestamp_index + 1
                if timestamp_index >= timestamp_len or timestamps[timestamp_index] * runtime_factor > FLAGS.runtime:
                    seen_last_scheduler_run = True
                    break

            if event_type == SUBMIT_EVENT:
                if seen_last_scheduler_run:
                    delays.append(FLAGS.runtime - timestamp * runtime_factor)
                else:
                    if task_id in scheduled_tasks:
                        delays.append(runtimes[timestamp_index])
                    else:
                        delays.append(FLAGS.runtime - timestamp * runtime_factor)
        csv_file.close()
    return delays


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
            if 'rapid' in delays:
                delays['rapid'].append(trace_delays)
            else:
                delays['rapid'] = [trace_delays]
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

    markers = {'rapid':'x', 'cost scaling':'o', 'relax':'+'}
    colors = {'rapid':'r', 'cost scaling':'b', 'relax':'g'}

    if FLAGS.paper_mode:
        plt.figure(figsize=(3.33, 2.22))
        set_paper_rcs()
    else:
        plt.figure()
        set_rcs()

    for algo, speedup_delays in delays.items():
        delays_98percentile = []
        delays_90percentile = []
        for delays in speedup_delays:
            delays_90percentile.append(np.percentile(delays, 90) / 1000 / 1000)
            delays_98percentile.append(np.percentile(delays, 98) / 1000 / 1000)
        print algo, "90percentile", delays_90percentile
        print algo, "98percentile", delays_98percentile
        plt.plot(speedups[:len(delays_98percentile)], delays_90percentile,
                 marker=markers[algo], color=colors[algo], mfc='none', mew=1.0,
                 mec=colors[algo], label=algo + ' 90th')
        plt.plot(speedups[:len(delays_98percentile)], delays_98percentile,
                 marker=markers[algo], color=colors[algo], mfc='none', mew=1.0,
                 mec=colors[algo], linestyle='--', label=algo + ' 98th')

    plt.ylabel('Scheduling delay at percentile [sec]')
    plt.ylim(0, 200)
    plt.xticks(speedups, speedups)
    plt.xlabel('Speedup')
    plt.legend(loc='lower right', frameon=False, handlelength=1.5,
               handletextpad=0.1, numpoints=1)
    plt.savefig("google_speedup_scheduling_delay.pdf",
                format="pdf", bbox_inches="tight")


if __name__ == '__main__':
  main(sys.argv)
