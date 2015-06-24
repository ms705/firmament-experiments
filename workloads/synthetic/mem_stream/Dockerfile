# A simple memory access test
FROM ubuntu:14.04

MAINTAINER Malte Schwarzkopf version: 0.1

RUN apt-get update && apt-get -y install linux-tools-common linux-tools-$(uname -r) && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY mem_stream /tmp/
COPY perf_helper.sh /tmp/
COPY run_mem_stream.sh /tmp/

ENV SIZE 1048576

CMD /tmp/run_mem_stream $SIZE
