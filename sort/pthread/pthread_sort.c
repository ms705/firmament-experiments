#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

typedef struct {
  unsigned char key[64];
} key;

typedef struct {
  int l;
  int r;
  int h;
} triple;

key *data;
pthread_attr_t attr;

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

void *threaded_merge_sort(void *param) {
  triple range = *(triple *)param;
  triple lrange;
  triple rrange;
  pthread_t lside;
  pthread_t rside;
  int p = range.l, q, r = range.r, n1, n2, n = r - p + 1, i, j, k;
  key *aleft, *aright;
  //  printf("%d %d\n", p, r);
  if (p < r) {
    if (range.h == 0) {
      qsort(data + p, n, sizeof(key), compare);
    } else {
      q = (p + r) >> 1;
      lrange.l = p, lrange.r = q, rrange.l = q + 1, rrange.r = r;
      lrange.h = range.h - 1;
      rrange.h = range.h - 1;
      pthread_create(&lside, &attr, threaded_merge_sort, (void *)&lrange);
      pthread_create(&rside, &attr, threaded_merge_sort, (void *)&rrange);
      pthread_join(lside, NULL);
      pthread_join(rside, NULL);
      n1 = q - p + 1, n2 = r - q;
      aleft = (key *)malloc(sizeof(key) * n1);
      aright = (key *)malloc(sizeof(key) * n2);
      for(i = 0; i < n1; aleft[i] = data[p+i], i++);
      for(i = 0; i < n2; aright[i] = data[q+1+i], i++);
      for(k = i = j = 0; k < n; k++) {
        if(i >= n1 || (j < n2 && compare(&aleft[i], &aright[j]) > 0)) {
          data[k+p] = aright[j++];
        } else {
          data[k+p] = aleft[i++];
        }
      }
      free(aleft);
      free(aright);
    }
  }
}

int main(int argc, char* argv[]) {
  int size;
  pthread_t sorter;
  triple range;

  if (argc < 4) {
    printf("Please pass input file name, number of rows and output file name.");
    return -1;
  }

  size = atol(argv[2]);
  get_data(&data, argv[1], size);

  pthread_attr_init(&attr);
  pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_JOINABLE);

  range.l = 0;
  range.r = size - 1;
  range.h = 5;

  pthread_create(&sorter, &attr, threaded_merge_sort, (void *)&range);
  pthread_join(sorter, NULL);

  pthread_attr_destroy(&attr);

  FILE *f = fopen(argv[3], "wb");
  fwrite(data, size, sizeof(key), f);

  fclose(f);

  /* int i;
  for (i = 0; i < size; ++i) {
    print_bytes(data[i].key);
    }*/
  return 0;
}
