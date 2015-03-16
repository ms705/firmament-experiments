#!/bin/bash

LIBMEMCACHED_VER=1.0.18

cd workloads/memaslap
wget https://launchpad.net/libmemcached/1.0/1.0.18/+download/libmemcached-${LIBMEMCACHED_VER}.tar.gz
tar -xvzf libmemcached-${LIBMEMCACHED_VER}.tar.gz
cd libmemcached-${LIBMEMCACHED_VER}

# configure and compile
LIBS=-lpthread ./configure --enable-memaslap
make -j12

echo [[ -f clients/memaslap ]]
