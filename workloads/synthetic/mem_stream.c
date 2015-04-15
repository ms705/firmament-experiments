#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

int main(int argc, char* argv[]) {
  // The only argument is the size of the buffer to work with, in bytes
  if (argc < 2) {
    printf("usage: mem_stream <buffer size>\n");
    exit(1);
  }
  int64_t buf_size = atol(argv[1]);
  // Allocate a big slab of memory
  uint64_t* buffer = (uint64_t*)malloc(buf_size);
  // Iterate over it, reading each word and swapping its bottom bit with the
  // previous word
  uint64_t j = 0;
  while (j < 100000000000ULL / buf_size) {
    //printf("Iteration %ju...\n", j);
    for (uint64_t i = 1; i < buf_size / sizeof(uint64_t); ++i) {
      uint64_t tmp = (buffer[i] & 0xfffffffffffffff0ULL) |
                     (buffer[i - 1] & 0xfULL);
      buffer[i-1] = (buffer[i - 1] & 0xfffffffffffffff0ULL) |
                    (buffer[i] & 0xfULL);
      buffer[i] = tmp;
    }
    ++j;
  }
}
