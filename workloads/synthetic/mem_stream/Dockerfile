# A simple memory access test
FROM ubuntu:14.04

MAINTAINER Malte Schwarzkopf version: 0.1

RUN apt-get update && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY mem_stream /usr/bin/

ENV SIZE 1048576

CMD ["/usr/bin/mem_stream"]
