# A simple sequential IO stream test
FROM ubuntu:14.04

MAINTAINER Malte Schwarzkopf version: 0.1

RUN apt-get update && apt-get -y install fio && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY *.fio /tmp/

ENV TEST_FILE /tmp/fio-seqread.fio

CMD /usr/bin/fio $TEST_FILE
