CC=gcc
CFLAGS=-std=c99
OPTFLAGS=-O3

all: hdfs_get

%: %.c
	$(CC) -o $@  $^ -I/home/srguser/firmament/build/third_party/libhdfs3/src/libhdfs3/src/client -L/home/srguser/firmament/build/third_party/libhdfs3/src/libhdfs3-build/src/ -lhdfs3 $(CFLAGS) $(OPTFLAGS)

clean:
	rm hdfs_get
