#!/usr/bin/python2.7
import sys
import gflags
import Queue
import time
import threading
import thriftpy
from datetime import datetime
from thriftpy.transport import TFramedTransportFactory

FLAGS = gflags.FLAGS
gflags.DEFINE_string('sparrow_thrift_path',
                     '/home/srguser/sparrow/src/main/thrift',
                     'Path to the Sparrow Thrift definition files')
gflags.DEFINE_string('sparrow_frontend_host', '127.0.0.1',
                     'Sparrow scheduler hostname/IP')
gflags.DEFINE_integer('sparrow_frontend_port', 50201,
                      'Listening port for Sparrow frontend')
gflags.DEFINE_string('sparrow_scheduler_host', '127.0.0.1',
                     'Sparrow scheduler hostname/IP')
gflags.DEFINE_integer('sparrow_scheduler_port', 20503,
                      'Sparrow scheduler service port')

sparrow_service_thrift = thriftpy.load(
        FLAGS.sparrow_thrift_path + "/service.thrift",
        module_name="sparrow_service_thrift")
sparrow_types_thrift = thriftpy.load(
        FLAGS.sparrow_thrift_path + "/types.thrift",
        module_name="sparrow_types_thrift")

from thriftpy.rpc import make_client, make_server

tf = TFramedTransportFactory()

class SparrowClient:
  scheduler_client = None

  def __init__(self):
    # We need to run a FrontendService server, even though it does nothing in
    # practice
    fes = make_server(sparrow_service_thrift.FrontendService,
                      FLAGS.sparrow_frontend_host, FLAGS.sparrow_frontend_port,
                      trans_factory=tf)
    self.scheduler_client = make_client(sparrow_service_thrift.SchedulerService,
                                        FLAGS.sparrow_scheduler_host,
                                        FLAGS.sparrow_scheduler_port,
                                        trans_factory=tf)

    self.scheduler_client.registerFrontend("clusterMixApp",
                                           FLAGS.sparrow_frontend_host + ":" +
                                           str(FLAGS.sparrow_frontend_port))

  def submit_job(self, job_id, job_type, num_tasks):
    request = sparrow_types_thrift.TSchedulingRequest()
    request.app = "clusterMixApp"

    task_specs = []
    for i in range(num_tasks):
      task_spec = sparrow_types_thrift.TTaskSpec()
      task_spec.taskId = str(job_id * 100000) + str(i)
      task_spec.preference = sparrow_types_thrift.TPlacementPreference()
      # Task type: 0 = CPU spin, 1 = HDFS get
      task_spec.message = chr(0) + chr(0) + chr(0) + chr(job_type)
      task_specs.append(task_spec)
    request.tasks = task_specs

    request.user = sparrow_types_thrift.TUserGroupInfo()

    self.scheduler_client.submitJob(request)


  def replay_workload(self):
    events = Queue.PriorityQueue()
    index = 0
    for i in range(0, 96000, 8000):
      for task_index in range(0, 2):
        events.put((i, (index, 1)))
        events.put((i, (index + 1, 0)))
        events.put((i, (index + 2, 0)))
        index += 3
    for i in range(2000, 96000, 8000):
      for task_index in range(0, 8):
        events.put((i, (index, 2 + task_index)));
        events.put((i, (index + 1, 0)))
        events.put((i, (index + 2, 0)))
        index += 3
    for i in range(6000, 96000, 8000):
      for task_index in range(0, 16):
        events.put((i, (index, 10 + task_index)));
        events.put((i, (index + 1, 0)))
        events.put((i, (index + 2, 0)))
        index += 3

    start_time = datetime.now()
    threads = []
    while events.empty() is False:
      (run_at_time, (task_index, task_type)) = events.get()
      time_diff = datetime.now() - start_time
      time_now_ms = (time_diff.days * 24 * 60 * 60 + time_diff.seconds) * 1000 + time_diff.microseconds / 1000
      if run_at_time <= time_now_ms:
        print '... Running at: ', time_now_ms
        run_thread = threading.Thread(target=self.submit_job, args=(task_index, task_type, 1))
        run_thread.start()
        if run_thread.is_alive():
          print "... running (%s)" % (task_index)
          threads.append(run_thread)
        else:
          print "... ERROR"
      else:
        events.put((run_at_time, (task_index, task_type)))

    for thread in threads:
      if thread.is_alive():
        while thread.is_alive():
          print "Error: thread is still alive"
          time.sleep(1)
        thread.join()
      else:
        thread.join()


def main(argv):
  try:
    argv = FLAGS(argv)
  except gflags.FlagsError as e:
    print('%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS))

  sc = SparrowClient()

  sc.replay_workload()

if __name__ == '__main__':
  main(sys.argv)
