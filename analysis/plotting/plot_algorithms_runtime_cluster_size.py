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
    markers = {'cycle cancelling':'x', 'cost scaling':'o', 'relax':'+',
               'succ. shortest':'^'}
    colors = {'cycle cancelling':'r', 'cost scaling':'b', 'relax':'g',
              'succ. shortest':'c'}
    if FLAGS.paper_mode:
        plt.figure(figsize=(3.33, 2.22))
        set_paper_rcs()
    else:
        plt.figure()
        set_rcs()
    index = 0
    print setups
    for algo, algo_runtimes in runtimes.items():
        plt.plot(range(0, len(algo_runtimes)),
                 [y / 1000.0 / 1000.0 for y in algo_runtimes],
                 label=algo, color=colors[algo], marker=markers[algo],
                 mfc='none', mew=1.0, mec=colors[algo])
        index = index + 1
    plt.yscale("log")
    plt.ylabel('Algorithm runtime')
    plt.ylim(0, FLAGS.max_runtime / 1000.0 / 1000.0)
    plt.yticks([10**x for x in range(-3, 3)],
               ["1ms", "10ms", "100ms", "1s", "10s", "100s"])
    plt.xlim(0, len(setups) - 1)
    plt.xticks(range(0, len(setups)),
               ["%u" % (float(x) * 12500) for x in setups], rotation=30,
               ha='right')
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
                if 'cost scaling' in runtimes:
                    runtimes['cost scaling'].append(avg_runtime)
                else:
                    runtimes['cost scaling'] = [avg_runtime]
            elif 'relax' in trace_path:
                if 'relax' in runtimes:
                    runtimes['relax'].append(avg_runtime)
                else:
                    runtimes['relax'] = [avg_runtime]
            elif 'successive_shortest' in trace_path:
                if 'succ. shortest' in runtimes:
                    runtimes['succ. shortest'].append(avg_runtime)
                else:
                    runtimes['succ. shortest'] = [avg_runtime]
            elif 'cycle_cancelling' in trace_path:
                if 'cycle cancelling' in runtimes:
                    runtimes['cycle cancelling'].append(avg_runtime)
                else:
                    runtimes['cycle cancelling'] = [avg_runtime]
            else:
                print 'Error: Unexpected algorithm'
    print runtimes
    plot_timeline('algorithms_scalability', runtimes,
                  [float(x) for x in setups])


if __name__ == '__main__':
  main(sys.argv)
