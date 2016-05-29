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
gflags.DEFINE_integer('max_runtime', 200000000, 'Do not show longer runs.')

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
    return runtimes


def plot_timeline(plot_file_name, runtimes, setups):
    markers = {'Cycle canceling':'x', 'Cost scaling':'o', 'Relaxation':'+',
               'Succ. shortest':'^'}
    colors = {'Cycle canceling':'r', 'Cost scaling':'b', 'Relaxation':'g',
              'Succ. shortest':'c'}
    if FLAGS.paper_mode:
        plt.figure(figsize=(3.33, 2.22))
        set_paper_rcs()
    else:
        plt.figure()
        set_rcs()
    setup_vals = [long(round(float(x) * 12500)) for x in setups]
    algo_order = ['Relaxation', 'Cost scaling', 'Succ. shortest', 'Cycle canceling']
    for algo in algo_order:
        algo_runtimes = runtimes[algo]
        plt.plot(setup_vals[:len(algo_runtimes)],
                 [y / 1000.0 / 1000.0 for y in algo_runtimes],
                 label=algo, color=colors[algo], marker=markers[algo],
                 mfc='none', mew=1.0, mec=colors[algo])

    plt.yscale("log")
    plt.ylabel('Average algorithm runtime')
    plt.yticks([10**x for x in range(-3, 3)],
               ["1ms", "10ms", "100ms", "1s", "10s", "100s"])
    plt.ylim(0.0003, FLAGS.max_runtime / 1000.0 / 1000.0)
    x_ticks = []
    index = 0
    for x in setup_vals:
        if index < 1 or index > 2:
            x_ticks.append(setup_vals[index])
        index += 1
    plt.xticks(x_ticks, [str(x) for x in x_ticks], rotation=30,
               ha='right')
    plt.xlim(0, 12500)
    plt.xlabel('Cluster size [machines]')

    plt.legend(loc='lower right', frameon=False, handlelength=1.5,
               handletextpad=0.1, numpoints=1)
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
            if 'cost_scaling' in trace_path:
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
                if 'Succ. shortest' in runtimes:
                    runtimes['Succ. shortest'].append(avg_runtime)
                else:
                    runtimes['Succ. shortest'] = [avg_runtime]
            elif 'cycle_cancelling' in trace_path:
                if 'Cycle canceling' in runtimes:
                    runtimes['Cycle canceling'].append(avg_runtime)
                else:
                    runtimes['Cycle canceling'] = [avg_runtime]
            else:
                print 'Error: Unexpected algorithm'
    print runtimes
    plot_timeline('algorithms_scalability', runtimes,
                  [float(x) for x in setups])


if __name__ == '__main__':
  main(sys.argv)
