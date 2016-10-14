# Copyright (c) 2016, Ionel Gog

import csv
import datetime
import dateutil.parser
import gflags
import math
import matplotlib
matplotlib.use("agg")
import os, sys
import matplotlib.pyplot as plt
import process_mesos_masterlog
from utils import *
from datetime import datetime

FLAGS = gflags.FLAGS
gflags.DEFINE_integer('num_files_to_process', 1,
                      'The number of trace files to process.')
gflags.DEFINE_bool('paper_mode', False, 'Adjusts the size of the plots.')
gflags.DEFINE_string('trace_paths', '',
                     ', separated list of path to trace files.')
gflags.DEFINE_string('trace_labels', '',
                     ', separated list of labels to use for trace files.')
gflags.DEFINE_string('ideal_runtimes_path', '',
                     'path the the file containing the ideal runtimes.')
gflags.DEFINE_string('docker_results_file', '',
                     'path to the file containing Docker results.')
gflags.DEFINE_string('kubernetes_results_file', '',
                     'path to the file containing Kubernetes results.')
gflags.DEFINE_string('mesos_log_file', '',
                     'path to the file containing Mesos master log.')
gflags.DEFINE_string('sparrow_results_file', '',
                     'path to the file containing Sparrow results.')
gflags.DEFINE_integer('xticks_increment', 20, 'Space between xticks.')
gflags.DEFINE_integer('max_x_value', 0, 'Maximum value on x-axis [0 = unset].')


SUBMIT_EVENT = 0
SCHEDULE_EVENT = 1
EVICT_EVENT = 2
FINISH_EVENT = 4

def get_ideal_runtimes(file_path):
    runtime_file = open(file_path)
    runtimes = []
    for line in runtime_file.readlines():
        vals = line.split(':')
        runtimes.append(long(vals[0]) * 60000000 + long(float(vals[1]) * 1000000))
    runtime_file.close()
    return runtimes


def get_scheduling_delays(trace_path):
    delays = []
    task_submit_time = {}
    tasks_submitted = set([])
    task_scheduled = {}
    tasks_on_machine = {}

    blacklisted_tasks = set([])
    try:
        csv_file = open(trace_path + "/blacklisted_tasks.csv")
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            task_id = long(row[0])
            blacklisted_tasks.add(task_id)
        csv_file.close()
    except IOError:
        print 'No blacklisted_tasks file'

    for num_file in range(0, FLAGS.num_files_to_process, 1):
        csv_file = open(trace_path + "/task_events/part-" +
                        '{:05}'.format(num_file) + "-of-00500.csv")
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            timestamp = long(row[0])
            task_id = (long(row[2]), long(row[3]))
            if long(row[3]) in blacklisted_tasks:
                continue
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


def plot_cdf(plot_file_name, cdf_vals, label_axis, labels, bin_width=1000):
    colors = {'Idle (isolation)' : 'y', 'Firmament' : 'r',
              'Docker SwarmKit' : 'k', 'Kubernetes' : 'g', 'Mesos' : 'c',
              'Sparrow' : 'm'}
    linestyles = {'Idle (isolation)' : 'solid', 'Firmament' : 'solid',
                  'Docker SwarmKit' : 'solid', 'Kubernetes' : 'solid',
                  'Mesos' : 'dotted', 'Sparrow' : 'solid'}
    markers = {'Idle (isolation)' : 'o', 'Firmament' : 'v',
               'Docker SwarmKit' : '^', 'Kubernetes' : '+',
               'Mesos' : '*', 'Sparrow' : 's'}
    if FLAGS.paper_mode:
        plt.figure(figsize=(3, 2))
        set_paper_rcs()
    else:
        plt.figure()
        set_rcs()

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
        max_x_val = max(max_val, FLAGS.max_x_value)
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

        perc_vals = [np.min(vals) / 1000.0 / 1000.0]
        for perc in range(1, 101):
            perc_vals.append(np.percentile(vals, perc) / 1000.0 / 1000.0)
        print perc_vals
        plt.plot(perc_vals, [float(x) / 100.0 for x in range(0, 101)],
                 label=labels[index], color=colors[labels[index]],
                 linestyle=linestyles[labels[index]], lw=1.0,
                 marker=markers[labels[index]], markevery=30, mew=0.8, ms=3,
                 mfc='none', mec=colors[labels[index]])
        index += 1

    max_x_val /= 1000 * 1000
    max_x_val = 177
    plt.xlim(0, max_x_val)
    plt.xticks(range(0, max_x_val, FLAGS.xticks_increment),
               [str(x) for x in range(0, max_x_val, FLAGS.xticks_increment)])
    plt.ylim(0, 1.0)
    plt.yticks(np.arange(0.0, 1.01, 0.2),
               [str(x) for x in np.arange(0.0, 1.01, 0.2)])
    plt.ylabel('CDF of task response time')
    plt.xlabel(label_axis)

    plt.legend(loc=4, frameon=False, handlelength=2.5, handletextpad=0.2)

    plt.savefig("%s.pdf" % plot_file_name,
                format="pdf", bbox_inches="tight")


def main(argv):
    try:
        argv = FLAGS(argv)
    except gflags.FlagsError as e:
        print('%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS))

    trace_paths = FLAGS.trace_paths.split(',')
    if FLAGS.trace_labels != '':
        labels = FLAGS.trace_labels.split(',')
    else:
        labels = []
    delays = []

    if FLAGS.trace_paths != '':
        for trace_path in trace_paths:
            trace_delays = get_scheduling_delays(trace_path)
            print 'Number of tasks: ', len(trace_delays)
            delays.append(trace_delays)

    if FLAGS.docker_results_file != '':
        docker_file = open(FLAGS.docker_results_file)
        csv_reader = csv.reader(docker_file)
        docker_runtimes = []
        for row in csv_reader:
            docker_runtimes.append(long(row[0]))
        print 'Number of Docker tasks: ', len(docker_runtimes)
        delays.append(docker_runtimes)
        labels.append('Docker SwarmKit')
        docker_file.close()

    if FLAGS.kubernetes_results_file != '':
        k8s_file = open(FLAGS.kubernetes_results_file)
        csv_reader = csv.reader(k8s_file)
        k8s_runtimes = []
        for row in csv_reader:
            created = dateutil.parser.parse(row[0])
            created_time = int(created.strftime("%s")) * 1000000 + created.microsecond
            finished = dateutil.parser.parse(row[2])
            finished_time = int(finished.strftime("%s")) * 1000000 + finished.microsecond
            k8s_runtimes.append(finished_time - created_time)
        print 'Number of Kubernetes tasks: ', len(k8s_runtimes)
        delays.append(k8s_runtimes)
        labels.append('Kubernetes')
        k8s_file.close()

    if FLAGS.mesos_log_file != '':
        raw_runtimes, raw_waittimes = process_mesos_masterlog.parse_master_log(FLAGS.mesos_log_file)
        mesos_response = []
        for task, runtime in raw_runtimes.iteritems():
            mesos_response.append(int((runtime + raw_waittimes[task]) * 1000000))
#        runtimes_in_sec = raw_runtimes.values()
#        mesos_runtimes = []
#        for runtime in runtimes_in_sec:
#            mesos_runtimes.append(int(runtime * 1000000))
        delays.append(mesos_response)
        labels.append('Mesos')

    if FLAGS.sparrow_results_file != '':
        sparrow_file = open(FLAGS.sparrow_results_file)
        csv_reader = csv.reader(sparrow_file)
        sparrow_runtimes = []
        for row in csv_reader:
            sparrow_runtimes.append(long(row[0]))
        print 'Number of Sparrow tasks: ', len(sparrow_runtimes)
        delays.append(sparrow_runtimes)
        labels.append('Sparrow')
        sparrow_file.close()

    delays.append(get_ideal_runtimes(FLAGS.ideal_runtimes_path))
    labels.append('Idle (isolation)')

    plot_cdf('task_response_time_cdf', delays, "Task response time [sec]",
             labels, bin_width=10000)


if __name__ == '__main__':
  main(sys.argv)
