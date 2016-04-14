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

def get_scheduler_runtimes(trace_path, column_index):
    # 0 timestamp
    # 1 solver runtime
    # 2 algorithm runtime
    # 3 total runtime (including Firmament)
    runtimes = []
    csv_file = open(trace_path + "/scheduler_events/scheduler_events.csv")
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        runtimes.append(long(row[column_index]))
    csv_file.close()
    return runtimes


def plot_timeline(plot_file_name, runtimes, setups):
    colors = ['b', 'r', 'g', 'c', 'm', 'y', 'k']
    if FLAGS.paper_mode:
        plt.figure(figsize=(3.33, 2.22))
        set_paper_rcs()
    else:
        plt.figure()
        set_rcs()
    index = 0
    max_y_val = 0
    for algo, algo_runtimes in runtimes.items():
        max_y_val = max(max_y_val, np.max(algo_runtimes))
        plt.plot(range(0, len(setups)),
                 [y / 1000.0 / 1000.0 for y in algo_runtimes],
                 label=algo, color=colors[index])
        index = index + 1
    plt.ylabel('Algorithm runtime [sec]')
    plt.ylim(0, max_y_val / 1000.0 / 1000.0)
    plt.xlim(0, len(setups) - 1)
    plt.xticks(range(0, len(setups)),
               ["%u" % (long(x)) for x in setups])
    plt.xlabel('Tasks per scheduling round')

    plt.legend(loc=2, frameon=False, handlelength=1.5, handletextpad=0.1)
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
                  [float(x) for x in setups])


if __name__ == '__main__':
  main(sys.argv)
