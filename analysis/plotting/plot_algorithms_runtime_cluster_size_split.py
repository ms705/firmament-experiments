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


def plot_timeline(plt, axes, start_index, end_index, runtimes, setups, first_run):
    markers = {'Cycle cancelling':'x', 'Cost scaling':'o', 'Relaxation':'+',
               'Succ. shortest':'^'}
    colors = {'Cycle cancelling':'r', 'Cost scaling':'b', 'Relaxation':'g',
              'Succ. shortest':'c'}
    a = plt.axes(axes)
    print setups
    handles = []
    for algo, algo_runtimes in runtimes.items():
        if len(algo_runtimes) > start_index:
            handle, = plt.plot(range(start_index, start_index + len(algo_runtimes[start_index:end_index])),
                               [y[1] / 1000.0 / 1000.0 for y in algo_runtimes[start_index:end_index]],
                               label=algo, color=colors[algo], marker=markers[algo],
                               mfc='none', mew=1.0, mec=colors[algo], lw=1.0)
            plt.errorbar(range(start_index, start_index + len(algo_runtimes[start_index:end_index])),
                         [y[1] / 1000.0 / 1000.0 for y in algo_runtimes[start_index:end_index]],
                         yerr=([y[0] / 1000.0 / 1000.0 for y in algo_runtimes[start_index:end_index]],
                               [y[2] / 1000.0 / 1000.0 for y in algo_runtimes[start_index:end_index]]),
                         color=colors[algo], lw=1.0)
            handles.append((handle, algo))

    plt.yscale("log")

    plt.xlim(start_index - 0.5, end_index - 0.5)
    xt_vals = ["%u" % (float(x) * 12500) for x in setups[start_index:end_index]]
    index = 0
    while index < len(xt_vals):
        print xt_vals[index]
        if int(xt_vals[index]) == 449:
            xt_vals[index] = 450
        index += 1
    plt.xticks(range(start_index, end_index),
               xt_vals, rotation=30, ha='center')

    plt.ylim(0.0003, FLAGS.max_runtime / 1000.0 / 1000.0)
    if first_run:
        plt.yticks([10**x for x in range(-3, 3)],
                   ["1ms", "10ms", "100ms", "1s", "10s", "100s"])
        plt.ylabel('Algorithm runtime [$\\log_{10}$]')
    else:
        plt.yticks([10**x for x in range(-3, 3)],
                   ["", "", "", "", "", ""])
    #     plt.tick_params(axis='y',which='both',left='off')

    return handles


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
            med_runtime = np.median(algo_runtime)
            perc_1st_runtime = np.percentile(algo_runtime, 1)
            perc_99th_runtime = np.percentile(algo_runtime, 99)
            runtime_tuple = (perc_1st_runtime, med_runtime, perc_99th_runtime)
            if 'cost_scaling' in trace_path:
                if 'Cost scaling' in runtimes:
                    runtimes['Cost scaling'].append(runtime_tuple)
                else:
                    runtimes['Cost scaling'] = [runtime_tuple]
            elif 'relax' in trace_path:
                if 'Relaxation' in runtimes:
                    runtimes['Relaxation'].append(runtime_tuple)
                else:
                    runtimes['Relaxation'] = [runtime_tuple]
            elif 'successive_shortest' in trace_path:
                if 'Succ. shortest' in runtimes:
                    runtimes['Succ. shortest'].append(runtime_tuple)
                else:
                    runtimes['Succ. shortest'] = [runtime_tuple]
            elif 'cycle_cancelling' in trace_path:
                if 'Cycle cancelling' in runtimes:
                    runtimes['Cycle cancelling'].append(runtime_tuple)
                else:
                    runtimes['Cycle cancelling'] = [runtime_tuple]
            else:
                print 'Error: Unexpected algorithm'
    print runtimes
    fake_tuple = (FLAGS.max_runtime + 1000000000,
                  FLAGS.max_runtime + 1000000000,
                  FLAGS.max_runtime + 1000000000)
    runtimes['Cycle cancelling'].append(fake_tuple)
    runtimes['Cycle cancelling'].append(fake_tuple)
    runtimes['Cycle cancelling'].append(fake_tuple)
    runtimes['Cycle cancelling'].append(fake_tuple)
    runtimes['Cycle cancelling'].append(fake_tuple)

    if FLAGS.paper_mode:
        plt.figure(figsize=(2.4, 1.6))
        set_paper_rcs()
    else:
        plt.figure()
        set_rcs()

    start_index = 0
    end_index = 4
    h1 = plot_timeline(plt, [0.0, 0.0, 0.44, 1.0], start_index, end_index, runtimes, [float(x) for x in setups], True)
    start_index = 4
    end_index = 9
    h2 = plot_timeline(plt, [0.44, 0., .56, 1.], start_index, end_index, runtimes, [float(x) for x in setups], False)

    plt.xlabel('Cluster size [machines]', x=0.1)

    order = {'Cycle cancelling': 0, 'Succ. shortest': 1, 'Cost scaling': 2,
             'Relaxation': 3}
    leg_entries = sorted(h2, key=lambda k: order[k[1]])
    plt.legend(zip(*leg_entries)[0], zip(*leg_entries)[1], loc='lower right',
               frameon=False, handlelength=1.5, handletextpad=0.1, numpoints=1)
    plt.savefig("algorithms_scalability.pdf", format="pdf", bbox_inches="tight")



if __name__ == '__main__':
  main(sys.argv)
