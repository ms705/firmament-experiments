import sys, os, errno
import pycurl
import json
import subprocess, shlex
from StringIO import StringIO

def mkdir_p(path):
  try:
    os.makedirs(path)
  except OSError as exc: # Python >2.5
    if exc.errno == errno.EEXIST and os.path.isdir(path):
      pass
    else: raise

def grab_url(url):
  buffer = StringIO()
  c = pycurl.Curl()
  c.setopt(c.URL, url)
  c.setopt(c.WRITEDATA, buffer)
  c.perform()
  c.close()
  return buffer.getvalue()

if len(sys.argv) < 4:
  print "usage: pull_job_data.py <coordinator hostname> <webUI port> <output dir> [grab logs]"
  sys.exit(1)

if len(sys.argv) == 5:
  grab_logs = bool(sys.argv[4])
else:
  grab_logs = False

body = grab_url('http://%s:%d/jobs/?json=1' % (sys.argv[1], int(sys.argv[2])))

body_dec = json.loads(body)

for name, jobid in body_dec.items():
  print "Getting %s (%s)..." % (name, jobid)
  data = grab_url('http://%s:%d/job/dtg/?id=%s' % (sys.argv[1], int(sys.argv[2]), jobid))

  cat = name[0:name.rfind("/")]
  run = name[name.rfind("/") + 1:]
  print cat
  try:
    mkdir_p(sys.argv[3] + "/" + cat)
  except OSError:
    pass
  fd = open(sys.argv[3] + "/" + cat + "/" + run, "w")
  fd.write(data)
  fd.close()

  # grab logs
  if grab_logs:
    logdir = sys.argv[3] + "/logs/" + jobid
    mkdir_p(logdir)
    command = "/home/srguser/firmament-experiments/analysis/scripts/collect_job_logs.sh %s http://%s:%d %s/" % (jobid, sys.argv[1], int(sys.argv[2]), logdir)
    subprocess.call(shlex.split(command))
