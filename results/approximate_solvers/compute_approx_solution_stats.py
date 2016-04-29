# Copyright (c) 2016, Ionel Gog

import gflags
import os, sys

FLAGS = gflags.FLAGS
gflags.DEFINE_string('optimal_output_log_path', '',
                     'path to the log of the optimal solution')
gflags.DEFINE_string('approximate_output_log_path', '',
                     'path to the log of the approximate log')

def main(argv):
    try:
        argv = FLAGS(argv)
    except gflags.FlagsError as e:
      print('%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS))

    approx_task_to_pu = {}
    with open(FLAGS.approximate_output_log_path) as f:
        for line in f:
            if line[0] == 'm' and line[1] == ' ':
                line_vals = line.strip('\n').split(' ')
                task_id = long(line_vals[1])
                pu_id = long(line_vals[2])
                approx_task_to_pu[task_id] = pu_id

    tasks_to_pu = {}
    num_migrated_tasks = 0
    num_evicted_tasks = 0
    with open(FLAGS.optimal_output_log_path) as f:
        for line in f:
            if line[0] == 'm' and line[1] == ' ':
                line_vals = line.strip('\n').split(' ')
                task_id = long(line_vals[1])
                pu_id = long(line_vals[2])
                if task_id in approx_task_to_pu:
                    if approx_task_to_pu[task_id] != pu_id:
                        num_migrated_tasks = num_migrated_tasks + 1
                else:
                    num_evicted_tasks = num_evicted_tasks + 1
                tasks_to_pu[task_id] = pu_id
    num_other_tasks_scheduled = 0
    for task_id, pu_id in approx_task_to_pu.iteritems():
        if task_id not in tasks_to_pu:
            num_other_tasks_scheduled = num_other_tasks_scheduled + 1
    print FLAGS.approximate_output_log_path, num_evicted_tasks, num_migrated_tasks, num_other_tasks_scheduled


if __name__ == '__main__':
  main(sys.argv)
