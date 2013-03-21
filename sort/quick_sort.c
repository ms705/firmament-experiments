#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
  unsigned char key[64];
} key;

int compare(const key* left, const key* right) {
  int i = 0;
  for (; i < 64; i++) {
    if (left->key[i] < right->key[i]) {
      return -1;
    }
    if (left->key[i] > right->key[i]) {
      return 1;
    }
  }
  return 0;
}

void print_bytes(const unsigned char* bytes) {
  int i;
  for (i = 0; i < 64; i++) {
    printf("%x ", bytes[i]);
  }
  printf("\n");
}

void get_data(key **data, const char* file_name, int size) {
  int num_vals;
  int const_size;
  key value;
  key *data_loc;
  //  unsigned char *buffer = (unsigned char*)malloc(sizeof(unsigned char) * 104);
  FILE *f = fopen(file_name, "rb");

  if (f == NULL) {
    printf("Could not open file");
    return;
  }
  //  fread(buffer, sizeof(unsigned char), 104, f);
  data_loc = (key*)calloc(size, sizeof(key));
  for (num_vals = 0; num_vals < size; num_vals++) {
    fread(&const_size, sizeof(int), 1, f);
    fread(&data_loc[num_vals], sizeof(key), 1, f);
    fread(&const_size, sizeof(int), 1, f);
    fread(&value, sizeof(key), 1, f);
    // Read (k,v) delimiter.
    fread(&const_size, sizeof(int), 1, f);
    // print_bytes(data_loc[num_vals].key);
  }
  fclose(f);
  *data = data_loc;
}

int main(int argc, char* argv[]) {
  int size;
  key *data;
  int my_rank;
  int num_proc;
  if (argc < 4) {
    printf("Please pass input file name, number of rows and output file name.");
    return -1;
  }
  size = atol(argv[2]);
  get_data(&data, argv[1], size);
  qsort(data, size, sizeof(key), compare);
  FILE *f = fopen(argv[3], "wb");
  fwrite(data, size, sizeof(key), f);
  fclose(f);
  /*  int i;
  for (i = 0; i < size; ++i) {
    print_bytes(data[i].key);
  }*/
  return 0;
}
