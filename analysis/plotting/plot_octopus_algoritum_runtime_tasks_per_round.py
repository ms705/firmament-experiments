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
gflags.DEFINE_string('trace_paths', '',
                     ', separated list of path to trace files.')
gflags.DEFINE_string('setups', '', ', separated list of cluster setups.')
gflags.DEFINE_integer('runtimes_after_timestamp', 0,
                      'Only plot runtimes of runs that happened after.')


def get_scheduler_runtimes(trace_path, column_index):
    # 0 timestamp
    # 1 solver runtime
    # 2 algorithm runtime
    # 3 total runtime (including Firmament)
    runtimes = []
    csv_file = open(trace_path + "/scheduler_events/scheduler_events.csv")
    csv_reader = csv.reader(csv_file)
    index = 0
    for row in csv_reader:
        timestamp = long(row[0])
        if timestamp > FLAGS.runtimes_after_timestamp:
            if index % 2 == 0:
                runtimes.append(long(row[column_index]))
            index = index + 1
    csv_file.close()
    return runtimes


def plot_timeline(plot_file_name, runtimes, setups):
    markers = {'cycle cancelling':'x', 'Cost scaling':'o', 'Relaxation':'+',
               'succ. shortest':'^'}
    colors = {'cycle cancelling':'r', 'Cost scaling':'b', 'Relaxation':'g',
              'succ. shortest':'c'}
    if FLAGS.paper_mode:
        plt.figure(figsize=(3, 2))
        set_paper_rcs()
    else:
        plt.figure()
        set_rcs()
    max_y_val = 0
    for algo, algo_runtimes in reversed(runtimes.items()):
        runtimes_in_sec = [[x / 1000 / 1000 for x in y] for y in algo_runtimes]
        max_y_val = max(max_y_val, np.max(runtimes_in_sec))
        plt.errorbar(setups,
                     [np.mean(vals) for vals in runtimes_in_sec],
                     yerr=[np.std(vals) for vals in runtimes_in_sec],
                     color=colors[algo],
                     label=algo,
                     marker=markers[algo],
                     mfc='none', mec=colors[algo], mew=1.0, lw=1.0, markevery=2)
        # plt.plot(setups,
        #          [np.mean(y) / 1000.0 / 1000.0 for y in algo_runtimes],
        #          label=algo, color=colors[algo], marker=markers[algo],
        #          mfc='none', mec=colors[algo], mew=1.0, lw=1.0)
    plt.ylabel('Algorithm runtime [sec]')
    max_x_val = setups[-1]
    plt.xticks(range(0, max_x_val + 1, 1000),
               ["%u" % x for x in range(0, max_x_val + 1, 1000)])
    plt.yticks(range(0, max_y_val, 5),
               [str(x) for x in range(0, max_y_val, 5)])
    plt.xlim(0, max_x_val)
    print max_y_val
    plt.xlabel('Tasks in arriving job')

    plt.legend(loc=2, frameon=False, handlelength=1.5, handletextpad=0.1,
               numpoints=1)
    plt.savefig("%s.pdf" % plot_file_name,
                format="pdf", bbox_inches="tight")


def main(argv):
    try:
        argv = FLAGS(argv)
    except gflags.FlagsError as e:
        print('%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS))

    trace_paths = FLAGS.trace_paths.split(',')
    setups = FLAGS.setups.split(',')
    runtimes = {}
    num_entries = len(setups)
    for trace_path in trace_paths:
        algo_runtime = get_scheduler_runtimes(trace_path, 2)
        # XXX(malte): hack to deal with cs2 not providing this info
        if algo_runtime[0] != 18446744073709551615:
            if 'cost_scaling' in trace_path:
                if 'Cost scaling' in runtimes:
                    runtimes['Cost scaling'].append(algo_runtime)
                else:
                    runtimes['Cost scaling'] = [algo_runtime]
            elif 'relax' in trace_path:
                if 'Relaxation' in runtimes:
                    runtimes['Relaxation'].append(algo_runtime)
                else:
                    runtimes['Relaxation'] = [algo_runtime]
            elif 'successive_shortest' in trace_path:
                if 'successive shortest' in runtimes:
                    runtimes['successive shortest'].append(algo_runtime)
                else:
                    runtimes['successive shortest'] = [algo_runtime]
            elif 'cycle_cancelling' in trace_path:
                if 'cycle cancelling' in runtimes:
                    runtimes['cycle cancelling'].append(algo_runtime)
                else:
                    runtimes['cycle cancelling'] = [algo_runtime]
            else:
                print 'Error: Unexpected algorithm'
    print runtimes
    plot_timeline('algorithms_runtime_tasks_per_round', runtimes,
                  [long(x) for x in setups])


if __name__ == '__main__':
  main(sys.argv)
