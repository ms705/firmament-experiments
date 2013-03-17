/**
 * Exercise a limited-depth-tree parallel merge sort under MPI.
 *
 * This works best if the number of processes in the communicator
 * is an exact power of two.  Then at the leaf level all processes
 * are computing and then (where the "parent" is not the node
 * itself) sending the results back to the parent.
 *
 * Author:  Timothy Rolfe
 */
#include <stdio.h>
#include <stdlib.h>     // for rand, etc.
#include <time.h>       // for time(NULL)
#include <mpi.h>

//#define  DEBUG

#define  INIT  1        // Message giving size and height
#define  DATA  2        // Message giving vector to sort
#define  ANSW  3        // Message returning sorted vector
#define  FINI  4        // Send permission to terminate

// Required by qsort()
int compare ( const void* left, const void* right );  // for qsort()

// Parallel merge logic under MPI
void parallelMerge ( long *vector, int size, int myHeight );

// Generate a vector of random data for a size.  Modify the
// variables vector and size by writing through the pointers
// passed (i.e., pointer to long* and pointer to int).
void getData ( long **vPtr, int *sizePtr );

// Verify the array:  for all k, x[k] = k+1
int  validate ( long *vector, int size );

int main ( int argc, char* argv[] )
{
   int myRank, nProc;
   int rc;
   int   size;          // Size of the vector being sorted
   long *vector,        // Vector for parallel sort
        *solo;          // Copy for sequential sort
   double start,        // Begin parallel sort
          middle,       // Finish parallel sort
          finish;       // Finish sequential sort

   rc = MPI_Init(&argc, &argv);
   srand(time(NULL));// Set up for shuffling

   if ( rc < 0 )
   {
      puts ("Failed to enroll in MPI.  Abort!");
      exit(-1);
   }

   if ( argc > 1 )
      size = atoi(argv[1]);
   rc = MPI_Comm_rank (MPI_COMM_WORLD, &myRank);
   rc = MPI_Comm_size (MPI_COMM_WORLD, &nProc);

#ifdef DEBUG
   printf ("Started rank %d\n", myRank);  fflush(stdout);
#endif

   if ( myRank == 0 )        // Host process
   {
      int rootHt = 0, nodeCount = 1;

      while ( nodeCount < nProc )
      {  nodeCount += nodeCount; rootHt++;  }

      printf ("%d processes mandates root height of %d\n", nProc, rootHt);

      getData (&vector, &size);   // The vector to be sorted.

   // Capture time to sequentially sort the idential array
      solo = (long*) calloc ( size, sizeof *solo );
      memcpy (solo, vector, size * sizeof *solo);

      start = MPI_Wtime();
      parallelMerge ( vector, size, rootHt);
      middle = MPI_Wtime();
   }
   else                      // Node process
   {
      int   iVect[2],        // Message sent as an array
            height,          // Pulled from iVect
            parent;          // Computed from myRank and height
      MPI_Status status;     // required by MPI_Recv

      rc = MPI_Recv( iVect, 2, MPI_INT, MPI_ANY_SOURCE, INIT,
           MPI_COMM_WORLD, &status );
      size   = iVect[0];     // Isolate size
      height = iVect[1];     // and height
      vector = (long*) calloc (size, sizeof *vector);

      rc = MPI_Recv( vector, size, MPI_LONG, MPI_ANY_SOURCE, DATA,
           MPI_COMM_WORLD, &status );

      parallelMerge ( vector, size, height );

#ifdef DEBUG
      printf ("%d resigning from MPI\n", myRank); fflush(stdout);
#endif
      MPI_Finalize();
      return 0;
   }
// Only the rank-0 process executes here.

   qsort( solo, size, sizeof *solo, compare );

   finish = MPI_Wtime();

#ifdef DEBUG
      printf ("%d resigning from MPI\n", myRank); fflush(stdout);
#endif
   if ( validate ( vector, size ) )
      puts ("Sorting succeeds.");
   else
      puts ("SORTING FAILS.");

   printf ("  Parallel:  %3.3f\n", (middle-start) );
   printf ("Sequential:  %3.3f\n", (finish-middle) );
   printf ("  Speed-up:  %3.3f\n", (finish-middle)/(middle-start) );
   MPI_Finalize();
}

// If *sizePtr == 0, dialog with the user; otherwise use the
// specified size.  Generate a vector of that size, fill it
// so that x[k] = k+1, and then shuffle the vector.
int nextInt(int ceiling)
{  return (int) ((double)rand() * ceiling / RAND_MAX);  }

/**
 * Shuffle the entire array
 *
 * See Rolfe, Timothy.  "Algorithm Alley:  Randomized Shuffling",
 * Dr. Dobb's Journal, Vol. 25, No. 1 (January 2000), pp. 113-14.
 */
void shuffleArray ( long*  x, int lim )
{  while ( lim > 1 )
   {  int item;
      int save = x[lim-1];
      item = nextInt(lim);
      x[--lim] = x[item];                // Note predecrement on lim
      x[item] = save;
   } // end while
} // end shuffleArray()

// If *sizePtr == 0, dialog with the user; otherwise use the
// specified size.  Generate a vector of that size, fill it
// so that x[k] = k+1, and then shuffle the vector.
void getData ( long **vPtr, int *sizePtr )
{
   int   size;
   int   k;
   long *data;

   fputs ("Size:  ", stdout);
   if ( *sizePtr == 0 )
      scanf ("%d", &size);
   else
   {
      size = *sizePtr;
      printf ("%d\n", size);
   }
   data = (long*) calloc ( size, sizeof *data );
   for ( k = 0; k < size; k++ )
      data[k] = k+1;
   shuffleArray ( data, size );
   // Write the results back through the pointer parameters
   *vPtr = data;
   *sizePtr = size;
}

// Verify the array:  for all k, x[k] = k+1
int  validate ( long *vector, int size )
{
   int k;

   for ( k = 0; k < size; k++ )
      if ( vector[k] != k+1 )
         return 0;
   return 1;
}

// Required by qsort()
int compare ( const void* left, const void* right )
{
   long *lt = (long*) left,
        *rt = (long*) right,
         diff = *lt - *rt;

   if ( diff < 0 ) return -1;
   if ( diff > 0 ) return +1;
   return 0;
}

/**
 * Parallel merge logic under MPI
 *
 * The working core:  each internal node ships its right-hand
 * side to the proper node below it in the processing tree.  It
 * recurses on this function to process the left-hand side, as
 * the node one closer to the leaf level.
 */
void parallelMerge ( long *vector, int size, int myHeight )
{  int parent;
   int myRank, nProc;
   int rc, nxt, rtChild;

   rc = MPI_Comm_rank (MPI_COMM_WORLD, &myRank);
   rc = MPI_Comm_size (MPI_COMM_WORLD, &nProc);

   parent = myRank & ~(1<<myHeight);
   nxt = myHeight - 1;
   if ( nxt >= 0 )
      rtChild = myRank | ( 1 << nxt );

#ifdef DEBUG
   if ( myHeight > 0 )
      printf ("%#x -> %#x -> %#x among %d\n", parent, myRank, rtChild, nProc);
#endif
   if ( myHeight > 0 )
   {//Possibly a half-full node in the processing tree
      if ( rtChild >= nProc )     // No right child.  Move down one level
         parallelMerge ( vector, size, nxt );
      else
      {
         int   left_size  = size / 2,
               right_size = size - left_size;
         long *leftArray  = (long*) calloc (left_size, sizeof *leftArray),
              *rightArray = (long*) calloc (right_size, sizeof *rightArray);
         int   iVect[2];
         int   i, j, k;                // Used in the merge logic
         MPI_Status status;            // Return status from MPI

         memcpy (leftArray, vector, left_size*sizeof *leftArray);
         memcpy (rightArray, vector+left_size, right_size*sizeof *rightArray);
#ifdef DEBUG
         printf ("%d sending data to %d\n", myRank, rtChild); fflush(stdout);
#endif
         iVect[0] = right_size;
         iVect[1] = nxt;
         rc = MPI_Send( iVect, 2, MPI_INT, rtChild, INIT,
              MPI_COMM_WORLD);
         rc = MPI_Send( rightArray, right_size, MPI_LONG, rtChild, DATA,
              MPI_COMM_WORLD);

         parallelMerge ( leftArray, left_size, nxt );
#ifdef DEBUG
         printf ("%d waiting for data from %d\n", myRank, rtChild); fflush(stdout);
#endif
         rc = MPI_Recv( rightArray, right_size, MPI_LONG, rtChild, ANSW,
              MPI_COMM_WORLD, &status );

         // Merge the two results back into vector
         i = j = k = 0;
         while ( i < left_size && j < right_size )
            if ( leftArray[i] > rightArray[j])
               vector[k++] = rightArray[j++];
            else
               vector[k++] = leftArray[i++];
         while ( i < left_size )
            vector[k++] = leftArray[i++];
         while ( j < right_size )
            vector[k++] = rightArray[j++];
      }
   }
   else
   {
      qsort( vector, size, sizeof *vector, compare );
#ifdef DEBUG
      printf ("%d leaf sorting.\n", myRank); fflush(stdout);
#endif
   }

/**
 * Note:  If the computed parent is different from myRank, then
 * this is a right-hand side and needs to be sent as a message
 * back to its parent.  Otherwise, the "communication" is done
 * automatically because the result is generated in place.
 */
   if ( parent != myRank )
      rc = MPI_Send( vector, size, MPI_LONG, parent, ANSW,
           MPI_COMM_WORLD );
}
