# Copyright (c) 2016, Ionel Gog

import gflags
import os, sys

FLAGS = gflags.FLAGS
gflags.DEFINE_string('graph_path', '', 'path to the input graph')
gflags.DEFINE_string('output_log_path', '', 'path to the output log')


def main(argv):
    try:
        argv = FLAGS(argv)
    except gflags.FlagsError as e:
      print('%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS))
    nodes_type = {}
    with open(FLAGS.graph_path) as f:
        for line in f:
            if line[0] == 'n' and line[1] == ' ':
                line_vals = line.strip('\n').split(' ')
                node_id = long(line_vals[1])
                node_type = long(line_vals[3])
                nodes_type[node_id] = node_type

    with open(FLAGS.output_log_path) as f:
        for line in f:
            if line[0] == 'm' and line[1] == ' ':
                line_vals = line.strip('\n').split(' ')
                task_id = long(line_vals[1])
                pu_id = long(line_vals[2])
                if nodes_type[task_id] != 1 or nodes_type[pu_id] != 2:
                    print "Error: invalid mapping from", task_id, "to", pu_id


if __name__ == '__main__':
  main(sys.argv)
