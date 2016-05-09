// The Firmament project
// Copyright (c) 2016 Ionel Gog <ionel.gog@cl.cam.ac.uk>

#include <hdfs.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

int main(int argc, char* argv[]) {
  if (argc < 4) {
    printf("usage: hdfs_get <name node address> <name node port> <input file>\n");
    return 1;
  }
  // Sleep for 100ms.
  usleep(100 * 1000);
  struct hdfsBuilder* hdfs_builder = hdfsNewBuilder();
  if (!hdfs_builder) {
    printf("Could not create HDFS builder");
    return 1;
  }
  hdfsBuilderSetNameNode(hdfs_builder, argv[1]);
  int port = atoi(argv[2]);
  hdfsBuilderSetNameNodePort(hdfs_builder, port);
  hdfsBuilderConfSetStr(hdfs_builder, "dfs.client.read.shortcircuit", "false");
  hdfsFS fs = hdfsBuilderConnect(hdfs_builder);
  hdfsFreeBuilder(hdfs_builder);
  if (!fs) {
    printf("Could not connect to HDFS");
    return 1;
  }

  hdfsFile file_in = hdfsOpenFile(fs, argv[3], O_RDONLY, 0, 0, 0);
  char buffer[1048576];
  int done = 0;
  do {
    done = hdfsRead(fs, file_in, &buffer, 1048576);
  } while (done > 0);
  if (done < 0) {
    printf("Failed to read file: %s", hdfsGetLastError());
    return 1;
  }

  hdfsCloseFile(fs, file_in);
  hdfsDisconnect(fs);
  return 0;
}
