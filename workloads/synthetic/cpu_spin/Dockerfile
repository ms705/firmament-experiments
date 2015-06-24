# A simple CPU spinner task.
FROM ubuntu:14.04

MAINTAINER Malte Schwarzkopf version: 0.1

RUN apt-get update && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY cpu_spin /usr/bin/

ENV DURATION 10

CMD ["/usr/bin/cpu_spin"]
