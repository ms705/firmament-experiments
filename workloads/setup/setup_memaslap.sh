#!/bin/bash

LIBMEMCACHED_VER=1.0.18

mkdir -p workloads/memaslap
cd workloads/memaslap
wget https://launchpad.net/libmemcached/1.0/1.0.18/+download/libmemcached-${LIBMEMCACHED_VER}.tar.gz
tar -xvzf libmemcached-${LIBMEMCACHED_VER}.tar.gz
cd libmemcached-${LIBMEMCACHED_VER}

# patch statistics output
patch -p1 < ../patch_stats.diff

# configure and compile
LIBS=-lpthread ./configure --enable-memaslap
make -j12

if [ -f clients/memaslap ]; then
  exit 0
else
  exit 1
fi
