#!/bin/bash

function usage() {
  echo "usage: ./$(basename $0) [ -r|--experiment-root <path> -t|--trace-root <path>]"
}

while [[ $# -ge 1 ]]; do
  key="$1"

  case $key in
      -r|--experiment-root)
      EXPERIMENTS_ROOT="$2"
      shift # past argument
      ;;
      -t|--trace-root)
      TRACE_ROOT="$2"
      shift # past argument
      ;;
      -h|--help)
      usage
      exit 0
      ;;
      *)
      # unknown option
      ;;
  esac
  shift # past argument or value
done

if [[ ${EXPERIMENTS_ROOT} == "" || ${TRACE_ROOT} == "" ]]; then
  usage
  exit 1
fi

cd ${EXPERIMENTS_ROOT}/analysis/plotting/
python plot_algorithms_runtime_cluster_size_split.py \
  --setups="0.004,0.036,0.068,0.1,0.2,0.4,0.6,0.8,1.0" \
  --runtimes_after_timestamp=600000000 \
  --trace_paths=${TRACE_ROOT}/quincy/google_runtime_0.004events_flowlessly_cycle_cancelling/,${TRACE_ROOT}/quincy/google_runtime_0.004events_flowlessly_successive_shortest/,${TRACE_ROOT}/quincy/google_runtime_0.036events_flowlessly_successive_shortest/,${TRACE_ROOT}/quincy/google_runtime_0.068events_flowlessly_successive_shortest/,${TRACE_ROOT}/quincy/google_runtime_0.1events_flowlessly_successive_shortest/,${TRACE_ROOT}/quincy/google_runtime_0.2events_flowlessly_successive_shortest/,${TRACE_ROOT}/quincy/google_runtime_0.004events_flowlessly_relax/,${TRACE_ROOT}/quincy/google_runtime_0.036events_flowlessly_relax/,${TRACE_ROOT}/quincy/google_runtime_0.068events_flowlessly_relax/,${TRACE_ROOT}/quincy/google_runtime_0.1events_flowlessly_relax/,${TRACE_ROOT}/quincy/google_runtime_0.2events_flowlessly_relax/,${TRACE_ROOT}/quincy/google_runtime_0.4events_flowlessly_relax/,${TRACE_ROOT}/quincy/google_runtime_0.6events_flowlessly_relax/,${TRACE_ROOT}/quincy/google_runtime_0.8events_flowlessly_relax/,${TRACE_ROOT}/quincy/google_runtime_1.0events_flowlessly_relax/,${TRACE_ROOT}/quincy/google_86400_sec_quincy_preemption_bounded_1024MB_0.004events_flowlessly_cost_scaling/,${TRACE_ROOT}/quincy/google_runtime_0.036events_flowlessly_cost_scaling/,${TRACE_ROOT}/quincy/google_runtime_0.068events_flowlessly_cost_scaling/,${TRACE_ROOT}/quincy/google_86400_sec_quincy_preemption_bounded_1024MB_0.1events_flowlessly_cost_scaling/,${TRACE_ROOT}/quincy/google_86400_sec_quincy_preemption_bounded_1024MB_0.2events_flowlessly_cost_scaling/,${TRACE_ROOT}/quincy/google_86400_sec_quincy_preemption_bounded_1024MB_0.4events_flowlessly_cost_scaling/,${TRACE_ROOT}/quincy/google_86400_sec_quincy_preemption_bounded_1024MB_0.6events_flowlessly_cost_scaling/,${TRACE_ROOT}/quincy/google_86400_sec_quincy_preemption_bounded_1024MB_0.8events_flowlessly_cost_scaling/,${TRACE_ROOT}/quincy/google_86400_sec_quincy_preemption_bounded_1024MB_flowlessly_cost_scaling/ \
  --paper_mode
mv algorithms_scalability.pdf quincy_algorithms_cluster_scalability_split.pdf
