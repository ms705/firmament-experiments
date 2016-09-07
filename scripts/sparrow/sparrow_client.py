#!/usr/bin/python2.7
import sys
import gflags
import thriftpy
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
  sparrow_job_id = 0

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

  def submit_job(self, job_type, num_tasks):
    request = sparrow_types_thrift.TSchedulingRequest()
    request.app = "clusterMixApp"
  
    task_specs = []
    for i in range(num_tasks):
      task_spec = sparrow_types_thrift.TTaskSpec()
      task_spec.taskId = str(self.sparrow_job_id) + str(i)
      task_spec.preference = sparrow_types_thrift.TPlacementPreference()
      # Task type: 0 = CPU spin, 1 = HDFS get
      if job_type == 0:
        task_spec.message = chr(0) + chr(0) + chr(0) + chr(0)
      elif job_type == 1:
        task_spec.message = chr(0) + chr(0) + chr(0) + chr(1)
      task_specs.append(task_spec)
    request.tasks = task_specs

    request.user = sparrow_types_thrift.TUserGroupInfo()

    self.scheduler_client.submitJob(request)
    self.sparrow_job_id += 1


def main(argv):
  try:
    argv = FLAGS(argv)
  except gflags.FlagsError as e:
    print('%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS))

  sc = SparrowClient()

  for i in range(10):
    sc.submit_job(0, 2)

if __name__ == '__main__':
  main(sys.argv)
