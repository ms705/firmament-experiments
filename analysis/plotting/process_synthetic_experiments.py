#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
import numpy as np

def usage():
  print "usage: process_synthetic_experiments.py <folder>"

def process_perf_file(perf_file):
  out_dict = {}
  for line in open(perf_file).readlines():
    fields = line.split(",")
    if len(fields) < 2:
      continue
    assert len(fields) == 2
    if "." in fields[0]:
      out_dict[fields[1].strip()] = float(fields[0])
    else:
      out_dict[fields[1].strip()] = int(fields[0])
  return out_dict

def process_output(name_parts, out_file):
  pass

def ratio_vector(vec, key1, key2):
  out_vec = []
  for v in vec:
    out_vec.append(float(v[key1]) / float(v[key2]))
  return out_vec
 
def get_ipc(vec):
  return ratio_vector(vec, "instructions", "cycles")

def get_cpi(vec):
  return ratio_vector(vec, "cycles", "instructions")

def get_ipms(vec):
  return ratio_vector(vec, "instructions", "cpu/mem-stores/")

def get_ipcr(vec):
  return ratio_vector(vec, "instructions", "cache-references")

def get_cache_miss_ratio(vec):
  return ratio_vector(vec, "cache-misses", "cache-references")

def get_dist_str(v):
  return "μ: {: >15.5f}, σ: {: >15.5f}, 1%: {: >15.5f}, 50%: {: >15.5f}, 99%: {: >15.5f}".format(np.mean(v), np.std(v), np.percentile(v, 1), np.median(v), np.percentile(v, 99))

def load_perf_files_from_dir(input_dir):
  perf_results = {}
  for subdir, dirs, files in os.walk(input_dir):
    for file in files:
      #os.path.join(subdir, file)
      name_parts = file.split(".")
      assert len(name_parts) == 4
      workload = name_parts[0]
      setup = name_parts[1]
      hostname_exp = name_parts[2]
      if name_parts[-1] == "perf":
        # have a perf file
        perf_dict = process_perf_file(os.path.join(subdir, file))
        print perf_dict
        wl_setup_tup = (workload, setup)
        if not wl_setup_tup in perf_results:
          perf_results[wl_setup_tup] = [perf_dict]
        else:
          perf_results[wl_setup_tup].append(perf_dict)
      elif name_parts[-1] == "out":
        # program output
        process_output(name_parts, os.path.join(subdir, file))

  return perf_results
