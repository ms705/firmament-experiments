#!/bin/bash

# binary install -- can't currently use because we want the distributed runtime
#apt-get install python-pip python-dev
#pip install --upgrade https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.7.1-cp27-none-linux_x86_64.whl

# from-source install
git clone --recurse-submodules https://github.com/tensorflow/tensorflow workloads/tensorflow
sudo apt-get -y install python-numpy swig python-dev python-wheel

# Bazel
if [ -z $(which bazel) ]; then
  wget "https://github.com/bazelbuild/bazel/releases/download/0.2.0/bazel_0.2.0-jdk7-linux-x86_64.deb" -O /tmp/bazel_0.2.0-jdk7-linux-x86_64.deb
  sudo dpkg -i /tmp/bazel_0.2.0-jdk7-linux-x86_64.deb
fi

cd workloads/tensorflow

# This is a hack, since ./configure requires interactive operation
./util/python/python_config.sh --setup "$(which python)"

# package builder
bazel build -c opt //tensorflow/tools/pip_package:build_pip_package

# PIP package
bazel-bin/tensorflow/tools/pip_package/build_pip_package /tmp/tensorflow_pkg
sudo pip install /tmp/tensorflow_pkg/tensorflow-0.7.1-cp27-none-linux_x86_64.whl

# distributed runtime
bazel build -c opt //tensorflow/core/distributed_runtime/rpc:grpc_tensorflow_server
