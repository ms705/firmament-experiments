#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <mpi.h>

#define  INIT  1        // Message giving size and height
#define  DATA  2        // Message giving vector to sort
#define  ANSW  3        // Message returning sorted vector
#define  FINI  4        // Send permission to terminate

typedef struct {
  unsigned char key[64];
} key;

MPI_Datatype key_type;
MPI_Datatype type[1] = {MPI_UNSIGNED_CHAR};
int block_len[1] = {64};
MPI_Aint disp[1];

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

void parallel_merge(key *data, int size, int height) {
  int parent;
  int my_rank;
  int num_proc;
  int rc;
  int nxt;
  int rt_child;

  rc = MPI_Comm_rank(MPI_COMM_WORLD, &my_rank);
  rc = MPI_Comm_size(MPI_COMM_WORLD, &num_proc);
  parent = my_rank & ~(1 << height);
  nxt = height - 1;
  if (nxt >= 0) {
    rt_child = my_rank | (1 << nxt);
  }
  if (height > 0) {
    if (rt_child >= num_proc) {
      parallel_merge(data, size, nxt);
    } else {
      int left_size = size / 2;
      int right_size = size - left_size;
      key *left_array = (key*)calloc(left_size, sizeof(key));
      key *right_array = (key*)calloc(right_size, sizeof(key));
      int recv_vect[2];
      int i, j, k;
      MPI_Status status;
      memcpy(left_array, data, left_size * sizeof(key));
      memcpy(right_array, data + left_size, right_size * sizeof(key));
      recv_vect[0] = right_size;
      recv_vect[1] = nxt;
      rc = MPI_Send(recv_vect, 2, MPI_INT, rt_child, INIT, MPI_COMM_WORLD);
      rc = MPI_Send(right_array, right_size, key_type, rt_child, DATA,
                    MPI_COMM_WORLD);
      parallel_merge(left_array, left_size, nxt);
      //      parallel_merge(data, left_size, nxt);
      rc = MPI_Recv(right_array, right_size, key_type, rt_child, ANSW,
		    MPI_COMM_WORLD, &status);
      //      rc = MPI_Recv(data + left_size, right_size, key_type, rt_child, ANSW,
      //              MPI_COMM_WORLD, &status);
      for (i = 0, j = 0, k = 0; i < left_size && j < right_size; k++) {
        if (compare(&left_array[i], &right_array[j]) > 0) {
          data[k] = right_array[j++];
        } else {
          data[k] = left_array[i++];
        }
      }
      /*      for (i = 0, j = left_size; i < left_size || j < right_size; ) {
	if (compare(&data[j], &data[i]) < 0) {
  
	} else {
	  ++i;
	}
	}*/
      // TODO(ionel): Is struct assignment ok?
      // TODO(ionel): Change to memcpy.
      for (; i < left_size; data[k++] = left_array[i++]);
      for (; j < right_size; data[k++] = right_array[j++]);
      free(left_array);
      free(right_array);
    }
  } else {
    qsort(data, size, sizeof(key), compare);
  }
  if (parent != my_rank) {
    rc = MPI_Send(data, size, key_type, parent, ANSW, MPI_COMM_WORLD);
    free(data);
  }
}

int main(int argc, char* argv[]) {
  int size;
  key *data;
  int my_rank;
  int num_proc;
  double start_time;
  double end_read_time;
  double end_time;
  double end_write_time;
  key key_disp;
  int rc = MPI_Init(&argc, &argv);
  if (rc < 0) {
    printf("Failed to enroll MPI.");
    return -1;
  }
  if (argc < 4) {
    printf("Please pass input file name, number of rows and output file name.");
    return -1;
  }
  // Only one field in struct.
  disp[0] = 0;
  MPI_Type_create_struct(1, block_len, disp, type, &key_type);
  MPI_Type_commit(&key_type);

  size = atol(argv[2]);
  rc = MPI_Comm_rank(MPI_COMM_WORLD, &my_rank);
  rc = MPI_Comm_size(MPI_COMM_WORLD, &num_proc);

  if (my_rank == 0) { // Host process
    int root_ht = 0;
    int node_count = 1;
    for (; node_count < num_proc; node_count += node_count, root_ht++);
    start_time = MPI_Wtime();
    get_data(&data, argv[1], size);
    end_read_time = MPI_Wtime();
    parallel_merge(data, size, root_ht);
    end_time = MPI_Wtime();
  } else { // Node process
    int recv_vect[2];
    int height;
    int parent;
    MPI_Status status;
    rc = MPI_Recv(recv_vect, 2, MPI_INT, MPI_ANY_SOURCE, INIT, MPI_COMM_WORLD,
                  &status);
    size = recv_vect[0];
    height = recv_vect[1];
    data = (key*) calloc(size, sizeof(key));
    rc = MPI_Recv(data, size, key_type, MPI_ANY_SOURCE, DATA, MPI_COMM_WORLD,
                  &status);
    parallel_merge(data, size, height);
    MPI_Finalize();
    return 0;
  }

  FILE *f = fopen(argv[3], "wb");
  fwrite(data, size, sizeof(key), f);
  fclose(f);
  end_write_time = MPI_Wtime();
  printf("With Read & Write: %3.3lf\n", (end_write_time - start_time));
  printf("With Read: %3.3lf\n", (end_time - start_time));
  printf("Without Read: %3.3lf\n", (end_time - end_read_time));
  MPI_Finalize();

  /*  int i;
  for (i = 0; i < size; ++i) {
    print_bytes(data[i].key);
  }*/
  return 0;
}
