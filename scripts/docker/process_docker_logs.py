import datetime
import dateutil.parser
import gflags
import sys

FLAGS = gflags.FLAGS
gflags.DEFINE_string('log_file', '/var/log/upstart/docker.log',
                     'Path to the docker log file')
gflags.DEFINE_string('output_file', 'docker_task_response_time.csv',
                     'File to which to write response time')
gflags.DEFINE_string('blacklist_file', '',
                     'File which contains blaklisted tasks')

def main(argv):
  try:
      argv = FLAGS(argv)
  except gflags.FlagsError as e:
      print('%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS))

  blacklisted_tasks = set([])
  if FLAGS.blacklist_file != '':
      blacklist_file = open(FLAGS.blacklist_file)
      for line in blacklist_file.readlines():
          cline = line.strip('\n')
          blacklisted_tasks.add(cline)

  log_file = open(FLAGS.log_file)
  output_file = open(FLAGS.output_file, 'w')
  assignment_time = {}
  for line in log_file.readlines():
      if 'state.transition="COMPLETE->COMPLETE"' in line:
          entries = line.split(' ')
          completion = dateutil.parser.parse(entries[0].strip('"')[6:])
          completion_time = int(completion.strftime("%s")) * 1000000 + completion.microsecond
          task_id = line.split('task.id=')[1].rstrip()
          if task_id not in blacklisted_tasks:
              if task_id in assignment_time:
                  output_file.write(str(completion_time - assignment_time[task_id]) + '\n')
              else:
                  print 'ERROR: completion time for unassigned task %s' % (task_id)
#      elif 'state.transition="ASSIGNED->PREPARING"' in line or 'state.transition="ASSIGNED->ACCEPTED"' in line:
      elif '->RUNNING"' in line:
          entries = line.split(' ')
          assigned = dateutil.parser.parse(entries[0].strip('"')[6:])
          assigned_time = int(assigned.strftime("%s")) * 1000000 + assigned.microsecond
          task_id = line.split('task.id=')[1].rstrip()
          if task_id not in blacklisted_tasks:
              assignment_time[task_id] = assigned_time
  log_file.close()
  output_file.close()


if __name__ == '__main__':
    main(sys.argv)
