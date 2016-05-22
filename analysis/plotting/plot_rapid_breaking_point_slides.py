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
gflags.DEFINE_integer('runtimes_after_timestamp', 0,
                      'Only plot runtimes of runs that happened after.')
gflags.DEFINE_integer('runtimes_before_timestamp', 0,
                      'Only plot runtimes that happened before.')
gflags.DEFINE_string('rapid_100_nodes_traces', '',
                     ', separated list of path to trace files.')
gflags.DEFINE_string('rapid_100_nodes_labels', '',
                     ', separated list of labels to use for trace files.')
gflags.DEFINE_string('rapid_1000_nodes_traces', '',
                     ', separated list of path to trace files.')
gflags.DEFINE_string('rapid_1000_nodes_labels', '',
                     ', separated list of labels to use for trace files.')

SUBMIT_EVENT = 0
SCHEDULE_EVENT = 1


def get_placement_delays(trace_path):
    delays = []
    task_submit_time = {}
    tasks_scheduled = set([])
    tasks_submitted = set([])
    csv_file = open(trace_path)
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        if len(row) <= 5:
            break
        timestamp = long(row[0])
        task_id = (long(row[2]), long(row[3]))
        event_type = int(row[5])
        if timestamp >= FLAGS.runtimes_before_timestamp:
            continue
        if timestamp <= FLAGS.runtimes_after_timestamp:
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
                    delays.append(timestamp - submit_time)
            else:
                print ("Error: schedule event before submit event for task "
                       "(%s, %s)" % (row[2], row[3]))
                exit(1)
    csv_file.close()
    print trace_path, 'tasks submitted:', len(tasks_submitted)
    print trace_path, 'task scheduled:', len(tasks_scheduled)
    return delays


def main(argv):
    try:
        argv = FLAGS(argv)
    except gflags.FlagsError as e:
        print('%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS))

    if FLAGS.paper_mode:
        plt.figure(figsize=(3.33, 2.22))
        set_paper_rcs()
    else:
        plt.figure()
        set_rcs()

    if FLAGS.rapid_100_nodes_traces != '':
        rapid_100_nodes_traces = FLAGS.rapid_100_nodes_traces.split(',')
        labels = FLAGS.rapid_100_nodes_labels.split(',')
        delays = [260]
        for trace_path in rapid_100_nodes_traces:
            trace_delays = get_placement_delays(trace_path)
            delays.append(np.mean(trace_delays))
        print rapid_100_nodes_traces
        print delays

        index = 0
        total_runtime = []
        for label in labels:
            total_runtime.append(long(label) + delays[index] / 1000)
            index += 1
        x_vals = [3000 - long(x) for x in labels]
        print x_vals
        print total_runtime
        plt.plot(x_vals, total_runtime, color='r', label='Firmament 100 machines',
                 marker='v', mfc='none', mec='r', mew=1.0, lw=2)

    spark_x = [0, 1000, 1600, 2500]
    spark_y = [3000, 2350, 1950, 100000]

    plt.plot(spark_x, spark_y, color='green', label='Spark', marker='o',
             mfc='none', mec='green', mew=1.0, lw=2)


    # if FLAGS.rapid_1000_nodes_traces != '':
    #     rapid_1000_nodes_traces = FLAGS.rapid_1000_nodes_traces.split(',')
    #     labels = FLAGS.rapid_1000_nodes_labels.split(',')
    #     delays = [260]
    #     for trace_path in rapid_1000_nodes_traces:
    #         trace_delays = get_placement_delays(trace_path)
    #         delays.append(np.mean(trace_delays))
    #     print rapid_1000_nodes_traces
    #     print delays

    #     total_runtime = []
    #     index = 0
    #     for label in labels:
    #         total_runtime.append(long(label) + delays[index] / 1000)
    #         index += 1
    #     x_vals = [3000 - long(x) for x in labels]
    #     print x_vals
    #     print total_runtime
    #     plt.plot(x_vals, total_runtime, color='r', label='Firmament 1000 machines',
    #              marker='v', mfc='none', mec='r', mew=1.0, lw=2.0)

    ideal = [0, 1000, 2000, 2500, 2800, 2900, 3000]
    rev_ideal = [3000, 2000, 1000, 500, 200, 100, 0]
    # ideal = [0, 1000, 2000, 2200, 2400, 2625, 2800, 3000]
    # rev_ideal = [3000, 2000, 1000, 800, 600, 375, 200, 0]
    plt.plot(ideal, rev_ideal, color='black', label='Ideal', marker='x',
             mfc='none', mec='black', mew=1.0, lw=0.75)


    plt.ylabel('Task response time [ms]')
    plt.ylim(0, 3000)
    plt.xlim(0, 3000)

    plt.xticks(range(0, 3001, 500), range(3000, -1, -500))
    plt.xlabel('Task duration [ms]')
    plt.legend(loc='lower left', frameon=False, handlelength=1.5,
               handletextpad=0.2, numpoints=1)
    plt.savefig("rapid_breaking_point.pdf", format="pdf", bbox_inches="tight")


if __name__ == '__main__':
  main(sys.argv)
