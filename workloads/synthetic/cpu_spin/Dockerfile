# A simple CPU spinner task.
FROM ubuntu:14.04

MAINTAINER Malte Schwarzkopf version: 0.1

RUN apt-get update && apt-get -y install linux-tools-common linux-tools-$(uname -r) && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY cpu_spin /tmp/
COPY perf_helper.sh /tmp/
COPY run_cpu_spin.sh /tmp/

ENV DURATION 10

CMD /tmp/run_cpu_spin.sh $DURATION
