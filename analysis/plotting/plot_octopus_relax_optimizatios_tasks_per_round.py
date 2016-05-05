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
    markers = {'Cycle cancelling':'x', 'Cost scaling':'o',
               'Relaxation + arc prioritization':'+',
               'Succ. shortest':'^', 'Relaxation':'v'}
    colors = {'Cycle cancelling':'r', 'Cost scaling':'b',
              'Relaxation + arc prioritization':'g', 'Succ. shortest':'c',
              'Relaxation':'m'}
    if FLAGS.paper_mode:
        plt.figure(figsize=(3.33, 2.22))
        set_paper_rcs()
    else:
        plt.figure()
        set_rcs()
    max_y_val = 0
    for algo, algo_runtimes in runtimes.items():
#        max_y_val = max(max_y_val, np.max(algo_runtimes))
        runtimes_in_sec = [[x / 1000 / 1000 for x in y] for y in algo_runtimes]
        algo_name = ''
        if algo == 'Relaxation':
            algo_name = 'Relaxation + arc prioritization'
        elif algo == 'Relaxation without arc prioritization':
            algo_name = 'Relaxation'
        plt.errorbar(setups,
                     [np.mean(vals) for vals in runtimes_in_sec],
                     yerr=[np.std(vals) for vals in runtimes_in_sec],
                     color=colors[algo_name],
                     label=algo_name,
                     marker=markers[algo_name],
                     mfc='none', mec=colors[algo_name], mew=1.0, lw=1.0)
        # plt.plot(setups,
        #          [np.mean(y) / 1000.0 / 1000.0 for y in algo_runtimes],
        #          label=algo, color=colors[algo], marker=markers[algo],
        #          mfc='none', mec=colors[algo], mew=1.0, lw=1.0)
    plt.ylabel('Algorithm runtime [sec]')

    plt.xlim(0, 5000)
    plt.xticks(range(0, 5000 + 1, 1000),
               ["%u" % x for x in range(0, 5000 + 1, 1000)],
               rotation=30, ha='right')
    plt.xlabel('Tasks per scheduling round')

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
            if 'relax_without_arc_prioritization' in trace_path:
                if 'Relaxation without arc prioritization' in runtimes:
                    runtimes['Relaxation without arc prioritization'].append(algo_runtime)
                else:
                    runtimes['Relaxation without arc prioritization'] = [algo_runtime]
            elif 'cost_scaling' in trace_path:
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
                if 'Successive shortest' in runtimes:
                    runtimes['Successive shortest'].append(algo_runtime)
                else:
                    runtimes['Successive shortest'] = [algo_runtime]
            elif 'cycle_cancelling' in trace_path:
                if 'Cycle cancelling' in runtimes:
                    runtimes['Cycle cancelling'].append(algo_runtime)
                else:
                    runtimes['Cycle cancelling'] = [algo_runtime]
            else:
                print 'Error: Unexpected algorithm'
    print runtimes
    plot_timeline('algorithms_runtime_tasks_per_round', runtimes,
                  [long(x) for x in setups])


if __name__ == '__main__':
  main(sys.argv)
