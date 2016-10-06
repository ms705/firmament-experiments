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
    for row in csv_reader:
        timestamp = long(row[0])
        if timestamp > FLAGS.runtimes_after_timestamp:
            runtimes.append(long(row[column_index]))
    csv_file.close()
    return runtimes[:1]


def plot_timeline(plot_file_name, runtimes, setups):
    colors = {'Incremental cost scaling':'k', 'Cost scaling':'b',
              'Relaxation':'g'}
    markers = {'Incremental cost scaling':'^', 'Cost scaling':'o',
              'Relaxation':'+'}
    if FLAGS.paper_mode:
        plt.figure(figsize=(3, 2))
        set_paper_rcs()
    else:
        plt.figure()
        set_rcs()
    max_y_val = 0

    if 'Relaxation' in runtimes:
        algo = 'Relaxation'
        algo_runtimes = runtimes[algo]
        max_y_val = max(max_y_val, np.max(algo_runtimes))
        plt.plot(setups,
                 [y / 1000.0 / 1000.0 for y in algo_runtimes],
                 label=algo, color=colors[algo], marker=markers[algo],
                 mfc='none', mec=colors[algo], mew=1.0, lw=1.0)

    if 'Cost scaling' in runtimes:
        algo = 'Cost scaling'
        algo_runtimes = runtimes[algo]
        max_y_val = max(max_y_val, np.max(algo_runtimes))
        plt.plot(setups,
                 [y / 1000.0 / 1000.0 for y in algo_runtimes],
                 label=algo, color=colors[algo], marker=markers[algo],
                 mfc='none', mec=colors[algo], mew=1.0, lw=1.0)

    if 'Incremental cost scaling' in runtimes:
        algo = 'Incremental cost scaling'
        algo_runtimes = runtimes[algo]
        max_y_val = max(max_y_val, np.max(algo_runtimes))
        plt.plot(setups,
                 [y / 1000.0 / 1000.0 for y in algo_runtimes],
                 label=algo, color=colors[algo], marker=markers[algo],
                 mfc='none', mec=colors[algo], mew=1.0, lw=1.0)

    plt.ylabel('Algorithm runtime [sec]')
    plt.ylim(0, max_y_val / 1000.0 / 1000.0 + 35)
    max_x_val = setups[-1]
    plt.xlim(2500, max_x_val)
    plt.yticks(range(0, 451, 50), range(0, 451, 50))
    utilization = [float(144339 + x) / 161256 * 100 for x in setups]
    print setups
    x_ticks_vals = []
    for utilization in range(91, 101, 1):
        x_ticks_vals.append(utilization * 161256 / 100 - 144339)
    plt.xticks(x_ticks_vals, range(91, 101, 1))
    # plt.xticks(setups,
    #            ["%.2f" % x for x in utilization], rotation=30, ha='right')
    plt.xlabel('Cluster slot utilization [\%]')

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
            avg_runtime = np.mean(algo_runtime)
            if 'incremental_cost_scaling' in trace_path:
                if 'Incremental cost scaling' in runtimes:
                    runtimes['Incremental cost scaling'].append(avg_runtime)
                else:
                    runtimes['Incremental cost scaling'] = [avg_runtime]
            elif 'cost_scaling' in trace_path:
                if 'Cost scaling' in runtimes:
                    runtimes['Cost scaling'].append(avg_runtime)
                else:
                    runtimes['Cost scaling'] = [avg_runtime]
            elif 'relax' in trace_path:
                if 'Relaxation' in runtimes:
                    runtimes['Relaxation'].append(avg_runtime)
                else:
                    runtimes['Relaxation'] = [avg_runtime]
            elif 'successive_shortest' in trace_path:
                if 'successive shortest' in runtimes:
                    runtimes['successive shortest'].append(avg_runtime)
                else:
                    runtimes['successive shortest'] = [avg_runtime]
            elif 'cycle_cancelling' in trace_path:
                if 'cycle cancelling' in runtimes:
                    runtimes['cycle cancelling'].append(avg_runtime)
                else:
                    runtimes['cycle cancelling'] = [avg_runtime]
            else:
                print 'Error: Unexpected algorithm'
    print runtimes
    plot_timeline('algorithms_runtime_tasks_per_round', runtimes,
                  [long(x) for x in setups])


if __name__ == '__main__':
  main(sys.argv)
