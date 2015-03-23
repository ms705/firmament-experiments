import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys, os


def getSec(s):
  l = s.split(':')
  return int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2][0:2])

times = []
cpu_load = []
disk_rd = []
disk_wr = []
net_in = []
net_out = []
for l in open(sys.argv[1]).readlines():
  if l[0] == "#":
    continue
  fields = [x.strip() for x in l.split()]
  times.append(getSec(fields[0]))
  cpu_load.append(int(fields[1]))
  disk_rd.append(int(fields[5]))
  disk_wr.append(int(fields[7]))
  net_in.append(int(fields[9]))
  net_out.append(int(fields[11]))

plt.figure()

plt.plot(times, disk_rd, label="Disk read")
plt.plot(times, disk_wr, label="Disk write")
plt.plot(times, net_in, label="Net recv")
plt.plot(times, net_out, label="Net send")

plt.xlabel("Time [s]")
plt.ylabel("Throughput [KB/s]")

plt.legend()

#plt.show()
plt.savefig("tpch-timeline-305.pdf")
