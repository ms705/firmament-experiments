#!/usr/bin/python

baseline_best_medians = { 'mem_stream_1M_': 55.649999999999999,
                          'mem_stream_128K_': 55.590000000000003, 
                          'mem_stream_50M_': 56.990000000000002,
                          #'io_stream_read': 73.510000000000005,
                          'io_stream_read': 65.912184,
                          'mem_stream_1K': 52.939999999999998,
                          'io_stream_write': 29.620000000000001,
                          'cpu_spin': 60.0
                        }

baseline_caelum_medians = { 'mem_stream_1M_': 40.72000,
                            'mem_stream_128K_': 40.68000,
                            'mem_stream_50M_': 42.03500,
                            'io_stream_read': 36.61000,
                            'mem_stream_1K': 37.83000,
                            'io_stream_write': 17.86000,
                            'cpu_spin': 60.0
                        }

def normalize_by_baseline(workload, runtime, cluster="srg"):
  if cluster == "srg":
    normed = runtime / baseline_best_medians[workload]
    if normed < 0.9:
      print "WARNING: low normalized runtime for %s: %f (%f)" % (workload, runtime, normed)
    return normed
  elif cluster == "caelum":
    normed = runtime / baseline_caelum_medians[workload]
    if normed < 0.9:
      print "WARNING: low normalized runtime for %s: %f (%f)" % (workload, runtime, normed)
    return normed
  else:
    print "unknown cluster!"
    sys.exit(1)
  print runtime_date

