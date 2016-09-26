# Copyright (c) 2016, Ionel Gog

import csv
import gflags
import math
import matplotlib
matplotlib.use("agg")
import os, sys
import matplotlib.pyplot as plt
from collections import defaultdict
from utils import *

FLAGS = gflags.FLAGS
gflags.DEFINE_integer('num_files_to_process', 1,
                      'The number of trace files to process.')
gflags.DEFINE_bool('paper_mode', False, 'Adjusts the size of the plots.')
gflags.DEFINE_string('trace_paths', '',
                     ', separated list of path to trace files.')
gflags.DEFINE_string('trace_labels', '',
                     ', separated list of labels to use for trace files.')
gflags.DEFINE_integer('runtimes_after_timestamp', 0,
                      'Only plot runtimes of runs that happened after.')
gflags.DEFINE_integer('runtimes_before_timestamp', 0,
                      'Only plot runtimes that happened before.')


BYTES_TO_MB = 1048576
BYTES_TO_GB = 1073741824
BLOCK_SIZE_BYTES = 1073741824
BLOCK_ADD = 0
BLOCK_REMOVE = 1
MACHINE_ADD = 0
MACHINE_REMOVE = 1

SCHEDULE_EVENT = 1

def get_task_inputs(trace_path):
    csv_file = open(trace_path + "/tasks_to_blocks/tasks_to_blocks.csv")
    csv_reader = csv.reader(csv_file)
    task_blocks = defaultdict(list)
    for row in csv_reader:
        if len(row) < 3:
            print 'Reached truncated row'
            break

        job_id = long(row[0])
        task_index = long(row[1])
        block_id = long(row[2])
        task_blocks[(job_id, task_index)].append(block_id)
    csv_file.close()
    return task_blocks


def get_block_locations(trace_path):
    dfs_csv_file = open(trace_path + "/dfs_events/dfs_events.csv")
    dfs_csv_reader = csv.reader(dfs_csv_file)
    block_locations = defaultdict(list)
    for row in dfs_csv_reader:
        if len(row) < 5:
            print 'Reached truncated row'
            break
        timestamp = long(row[0])
        event_type = int(row[1])
        machine_id = long(row[2])
        block_id = long(row[3])
        block_size = long(row[4])
        if timestamp <= FLAGS.runtimes_after_timestamp:
            continue
        if timestamp >= FLAGS.runtimes_before_timestamp:
            continue
        if event_type == BLOCK_ADD:
            block_locations[block_id].append((timestamp, machine_id, block_size))
    dfs_csv_file.close()
    return block_locations


def get_machine_rack(trace_path):
    machines_racks_file = open(trace_path + "/machines_to_racks/machines_to_racks.csv")
    machines_racks_reader = csv.reader(machines_racks_file)
    machine_rack = {}
    for row in machines_racks_reader:
        if len(row) < 4:
            print 'Reached truncated row'
            break
        event_type = int(row[1])
        machine_id = long(row[2])
        rack_id = long(row[3])
        if event_type == MACHINE_ADD:
            machine_rack[machine_id] = rack_id
        else:
            print 'Reached unexpected event type'
            break
    machines_racks_file.close()
    return machine_rack


def get_task_locality(trace_path, task_blocks, blocks_locations, machine_rack):
    task_locality = []
    rack_locality = []
    tasks_scheduled = set([])
    total_local_data = 0
    total_rack_data = 0
    unique_blocks = set([])
    for num_file in range(0, FLAGS.num_files_to_process, 1):
        csv_file = open(trace_path + "/task_events/part-" +
                        '{:05}'.format(num_file) + "-of-00500.csv")
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if len(row) < 6:
                print 'Reached truncated row'
                break
            timestamp = long(row[0])
            task_id = (long(row[2]), long(row[3]))
            event_type = int(row[5])
            if timestamp <= FLAGS.runtimes_after_timestamp:
                continue
            if timestamp >= FLAGS.runtimes_before_timestamp:
                continue

            if event_type == SCHEDULE_EVENT and task_id not in tasks_scheduled:
                machine_id = long(row[4])
                tasks_scheduled.add(task_id)
                local_data_size = 0
                rack_data_size = 0
                total_data_size = 0
                num_local_blocks = 0
                for block_id in task_blocks[task_id]:
                    unique_blocks.add(block_id)
                    locations = blocks_locations[block_id]
                    # XXX(ionel): This is not quite correct. We should check
                    # the machine was still alive. However, machine failures
                    # are rare so they're not going to have an effect on the
                    # graph.
                    index = 0
                    for (timestamp, block_machine_id, block_size) in locations:
                        if index == 0:
                            total_data_size += block_size
                        index += 1
                        if machine_id == block_machine_id:
                            local_data_size += block_size
                            total_local_data += block_size
                            num_local_blocks += 1
                            break
                        if machine_id in machine_rack and block_machine_id in machine_rack:
                            if machine_rack[machine_id] == machine_rack[block_machine_id]:
                                rack_data_size += block_size
                                total_rack_data += block_size
                if total_data_size > 0:
                    task_locality.append(long(float(local_data_size) / float(total_data_size) * 100.0))
                    rack_locality.append(long(float(rack_data_size) / float(total_data_size) * 100.0))
#                    print total_data_size, local_data_size
#                    print len(task_blocks[task_id]), num_local_blocks

        csv_file.close()
    total_dfs_data = len(unique_blocks) * BLOCK_SIZE_BYTES
    return (total_dfs_data, total_local_data, total_rack_data, task_locality, rack_locality)


def plot_cdf(plot_file_name, cdf_vals, label_axis, labels, log_scale=False,
             bin_width=1000):
    colors = ['b', 'r', 'g', 'c', 'm', 'y', 'k']
    if FLAGS.paper_mode:
        plt.figure(figsize=(1.66, 1.11))
        set_paper_rcs()
    else:
        plt.figure()
        set_rcs()

    max_cdf_val = 0
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
        max_cdf_val = max(max_val, max_cdf_val)
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
        print " 90th: %f" % (perc90)
        perc99 = np.percentile(vals, 99)
        print " 99th: %f" % (perc99)

        bin_range = max_val - min_val + 1
        num_bins = bin_range / bin_width
        (n, bins, patches) = plt.hist(vals, bins=num_bins, log=False,
                                      normed=True, cumulative=True,
                                      histtype="step", color=colors[index])
        # hack to add line to legend
        plt.plot([-100], [-100], label=labels[index],
                 color=colors[index], linestyle='solid', lw=1.0)
        # hack to remove vertical bar
        patches[0].set_xy(patches[0].get_xy()[:-1])

        index += 1

    plt.xlim(0, 100)
    plt.xticks(range(0, 101, 20), range(0, 101, 20))

    plt.ylim(0, 1.0)
    plt.yticks(np.arange(0.0, 1.01, 0.2),
               [str(x) for x in np.arange(0.0, 1.01, 0.2)])

    plt.xlabel(label_axis)
    plt.ylabel('CDF of task data locality')

    plt.legend(loc='upper left', frameon=False, handlelength=2.5,
               handletextpad=0.2)

    plt.savefig("%s.pdf" % plot_file_name,
                format="pdf", bbox_inches="tight")


def plot_barchart(plot_file_name, percentage_local_data, ylabel, xlabels):
    colors = ['b', 'r', 'g', 'c', 'm', 'y', 'k']
    if FLAGS.paper_mode:
        plt.figure(figsize=(1.75, 1.11))
        set_paper_rcs()
    else:
        plt.figure()
        set_rcs()


    plt.bar(1, percentage_local_data[0], width=0.5, align="center",
            label=xlabels[0], color=colors[0])

    plt.bar(2, percentage_local_data[1], width=0.5, align="center",
            label=xlabels[1], color=colors[1])

    plt.ylim(0, 100)
    plt.xticks([1, 2], ['Quincy 14\%', 'Firmament 2\%'])
    plt.yticks(range(0, 101, 20), range(0, 101, 20))
    plt.xlabel('Preference threshold')
    plt.ylabel(ylabel)

    plt.savefig("%s.pdf" % plot_file_name,
                format="pdf", bbox_inches="tight")


def main(argv):
    try:
        argv = FLAGS(argv)
    except gflags.FlagsError as e:
        print('%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS))

    trace_paths = FLAGS.trace_paths.split(',')
    labels = FLAGS.trace_labels.split(',')
    task_localities = []
    rack_localities = []
    percentage_data_local = []
    percentage_data_rack = []
    machine_rack = {}
    for trace_path in trace_paths:
        task_blocks = get_task_inputs(trace_path)
        block_locations = get_block_locations(trace_path)
#        machine_rack = get_machine_rack(trace_path)
        (total_dfs_size, total_local_data, total_rack_data, task_locality, rack_locality) = get_task_locality(trace_path, task_blocks, block_locations, machine_rack)
        percentage_data_local.append(total_local_data * 100 / total_dfs_size)
        percentage_data_rack.append(total_rack_data * 100 / total_dfs_size)
        task_localities.append(task_locality)
        rack_localities.append(rack_locality)

    plot_barchart('task_percentage_local_bar_chart', percentage_data_local,
                  'Data read locally [\%]', labels)
#    plot_cdf('task_percentage_local_input_cdf', task_localities,
#             'Data locality [\%]', labels, log_scale=False, bin_width=1)


if __name__ == '__main__':
  main(sys.argv)
