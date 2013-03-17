/*
 *      MPI_MergeSort.c
 *      Implementation of parallel merge sort using MPI.
 *
 *      Copyright 2008 Auriza Akbar <auriza.akbar@gmail.com>
 *
 *      This program is free software; you can redistribute it and/or modify
 *      it under the terms of the GNU General Public License as published by
 *      the Free Software Foundation; either version 2 of the License, or
 *      (at your option) any later version.
 *
 *      This program is distributed in the hope that it will be useful,
 *      but WITHOUT ANY WARRANTY; without even the implied warranty of
 *      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *      GNU General Public License for more details.
 *
 *      USAGE: mpiexec -n [nprocs] MPI_MergeSort [datasize]
 */

#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

#define DEBUG
#define ROOT 0
#define ISPOWER2(x) (!((x)&((x)-1)))

/* Merge 2 arrays with same size */
long *merge(long array1[], long array2[], long size) {

    long *result = (long *)malloc(2*size*sizeof(long));
    long i=0, j=0, k=0;

    while ((i < size) && (j < size)) {
        result[k++] = (array1[i] <= array2[j])? array1[i++] : array2[j++];
    }
    while (i < size) {
        result[k++] = array1[i++];
    }
    while (j < size) {
        result[k++] = array2[j++];
    }

    return result;
}

/* Validate sorted data */
long sorted(long array[], long size) {
    long i;
    for (i=1; i<size; i++)
        if (array[i-1] > array[i])
            return 0;
    return 1;
}

/* Needed by qsort() */
int compare(const void *p1, const void *p2) {
   return *(long *)p1 - *(long *)p2;
}

int main(int argc, char** argv) {

    int i, b, nprocs, myrank;
    long datasize;
    long localsize, *localdata, *otherdata, *data = NULL;
    int active = 1;
    MPI_Status status;
    double start, finish, p, s;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &myrank);
    MPI_Comm_size(MPI_COMM_WORLD, &nprocs);

    /* Read datasize argument */
    datasize = (argc == 2)? atol(argv[1]) : nprocs*10;

    /* Check argument */
    if (!ISPOWER2(nprocs)) {
        if (myrank == ROOT) printf("Processor number must be power of two.\n");
        return MPI_Finalize();
    }
    if (datasize%nprocs != 0) {
        if (myrank == ROOT) printf("Datasize must be divisible by processor number.\n");
        return MPI_Finalize();
    }

    /* Generate data */
    if (myrank == ROOT) {
        data = (long *)malloc(datasize * sizeof(long));
        printf("Allocated a total of %jd bytes of memory!\n", datasize * sizeof(long));
        for (i = 0; i < datasize; i++) {
            data[i] = rand()%99 + 1;
        }
    }

    /* Start point of parallel processing */
    start = MPI_Wtime();

    /* Scatter data */
    localsize = datasize / nprocs;
    localdata = (long *) malloc(localsize * sizeof(long));
    MPI_Scatter(data, localsize, MPI_INT, localdata, localsize, MPI_INT, ROOT, MPI_COMM_WORLD);

    /* Sort localdata */
    qsort(localdata, localsize, sizeof(long), compare);

    /* Merge sorted data */
    for (b=1; b<nprocs; b*=2) {
        if (active) {
            if ((myrank/b)%2 == 1) {
                MPI_Send(localdata, b * localsize, MPI_INT, myrank - b, 1, MPI_COMM_WORLD);
                free(localdata);
                active = 0;
            } else {
                otherdata = (long *) malloc(b * localsize * sizeof(long));
                MPI_Recv(otherdata, b * localsize, MPI_INT, myrank + b, 1, MPI_COMM_WORLD, &status);
                localdata = merge(localdata, otherdata, b * localsize);
                free(otherdata);
            }
        }
    }

    /* End point of parallel processing */
    finish = MPI_Wtime();

    /* Runtime and speed-up analysis */
    if (myrank == ROOT) {

#ifdef DEBUG
        if (sorted(localdata, nprocs*localsize)) {
            printf("\nParallel sorting succeed.\n\n");
        } else {
            printf("\nParallel sorting failed.\n\n");
        }
#endif

        free(localdata);
        p = finish - start;
        printf("  Parallel : %.8f\n", p);

        /* Sequential sort */
        start = MPI_Wtime();
        qsort(data, datasize, sizeof(long), compare);
        finish = MPI_Wtime();

        free(data);
        s = finish - start;
        printf("Sequential : %.8f\n", s);

        printf("  Speed-up : %.8f\n\n", s/p);
    }

    return MPI_Finalize();
}
