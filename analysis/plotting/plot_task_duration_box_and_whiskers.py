# Copyright (c) 2016, Malte Schwarzkopf

import csv
import gflags
import math
import matplotlib
matplotlib.use("agg")
import os, sys
import matplotlib.pyplot as plt
from utils import *
from box_and_whisker import *

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
    delays.sort()
    return delays


def plot_scalability(plot_file_name, setups, runtimes,
                     x_label="",
                     y_label="Response time [s]"):
    if FLAGS.paper_mode:
        plt.figure(figsize=(3.33, 2.22))
        set_paper_rcs()
    else:
        plt.figure()
        set_rcs()

    ax = plt.gca()
    bp = percentile_box_plot(ax, runtimes, color='b')

    #plt.errorbar(range(1, len(setups) + 1), [np.mean(x) for x in runtimes],
    #             yerr=[np.std(x) for x in runtimes], marker="x")
    plt.xlim(0.5, len(setups) + 0.5)
    plt.ylim(ymin=0)
    plt.xticks(range(1, len(setups) + 1), setups, rotation=30, ha='right')
    plt.yticks(range(0, 120000001, 20000000), range(0, 121, 20))
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    plt.savefig("%s.pdf" % plot_file_name,
                format="pdf", bbox_inches="tight")


def main(argv):
    try:
        argv = FLAGS(argv)
    except gflags.FlagsError as e:
        print('%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS))

    trace_paths = FLAGS.trace_paths.split(',')
    labels = FLAGS.trace_labels.split(',')

    runtimes = []
    for t in trace_paths:
      runtimes.append(get_scheduling_delays(t))

    plot_scalability('task_duration_box_and_whiskers', labels, runtimes)


if __name__ == '__main__':
  main(sys.argv)
