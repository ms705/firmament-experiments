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
    if fields[0] == "<not supported>":
      continue
    if "." in fields[0]:
      out_dict[fields[1].strip()] = float(fields[0])
    else:
      out_dict[fields[1].strip()] = int(fields[0])
  return out_dict

def process_time_file(time_file):
  out_dict = {}
  total_time = 0.0
  for line in open(time_file).readlines():
    fields = line.split(":")
    if len(fields) < 2:
      continue
    label = fields[0].strip()
    if "Elapsed" in label:
      min_value = fields[4].strip()
      sec_value = fields[5].strip()
      total_time += 60.0 * float(min_value) + float(sec_value)
  out_dict["runtime"] = total_time
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

def get_ips(vec):
  return ratio_vector(vec, "instructions", "runtime")

def get_cpi(vec):
  return ratio_vector(vec, "cycles", "instructions")

def get_ipms(vec):
  assert len(vec) > 0
  if "cpu/mem-stores/" in vec[0]:
    ms_evt = "cpu/mem-stores/"
    ml_evt = "cpu/mem-loads/"
  else:
    ms_evt = "LLC-stores"
    ml_evt = "LLC-load-misses"
  ms_vec = [x[ms_evt] for x in vec]
  ml_vec = [x[ml_evt] for x in vec]
  in_vec = [x["instructions"] for x in vec]
  ipms_vec = []
  for i in range(len(in_vec)):
    ipms_vec.append(in_vec[i] / (ms_vec[i] + ml_vec[i]))
  return ipms_vec;

def get_ipcr(vec):
  return ratio_vector(vec, "instructions", "cache-references")

def get_ipcm(vec):
  return ratio_vector(vec, "instructions", "cache-misses")

def get_cache_miss_ratio(vec):
  return ratio_vector(vec, "cache-misses", "cache-references")

def get_runtime(vec):
  out_vec = []
  for v in vec:
    out_vec.append(float(v["runtime"]))
  return out_vec

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
      wl_setup_tup = (workload, setup)
      hostname = hostname_exp.split("-")[0]
      if not wl_setup_tup in perf_results:
        perf_results[wl_setup_tup] = { hostname: [] }
      if not hostname in perf_results[wl_setup_tup]:
        perf_results[wl_setup_tup][hostname] = []
      if name_parts[-1] == "perf":
        # have a perf file
        perf_dict = process_perf_file(os.path.join(subdir, file))
        # time measurement
        time_dict = process_time_file(os.path.join(subdir, ".".join(name_parts[0:-1]) + ".time"))
        perf_dict["runtime"] = time_dict["runtime"]
        perf_results[wl_setup_tup][hostname].append(perf_dict)
      elif name_parts[-1] == "out":
        # program output
        process_output(name_parts, os.path.join(subdir, file))
      elif name_parts[-1] == "time":
        # already processed above
        continue

  return perf_results
