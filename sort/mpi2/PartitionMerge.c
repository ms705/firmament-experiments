/**
 * Exercise a limited-depth-tree partitioned merge sort.  Proof of
 * concept before going to the parallel version.
 *
 * Author:  Timothy Rolfe
 */
#include <stdio.h>
#include <stdlib.h>     // for rand, etc.
#include <string.h>     // memcpy
#include <time.h>       // for time(NULL)
#include "wallClock.c"  // Apologies for including source code

//#define DEBUG           // Show communication structure

// Required by qsort()
int compare ( const void* left, const void* right );  // for qsort()

// Partition merge logic
void partitionedSort ( long *vector, int size, int myHeight, int me );

// Generate a vector of random data for a size.  Modify the
// variables vector and size by writing through the pointers
// passed (i.e., pointer to long* and pointer to int).
void getData ( long **vPtr, int *sizePtr );

// Verify the array:  for all k, x[k] = k+1
int  validate ( long *vector, int size );

int main ( int argc, char* argv[] )
{
   int    height;       // Height of the root in the sorting tree
   int    size = 0;     // Size of the vector being sorted
   long  *vector,       // Vector for partitioned sort
         *solo;         // Copy for sequential sort
   double start,        // Begin partitioned sort
          middle,       // Finish partitioned sort
          finish;       // Finish sequential sort

   srand(time(NULL));// Set up for shuffling

   if ( argc > 1 )
      size = atoi(argv[1]);

   fputs ("Root height:  ", stdout);
   if ( argc > 2 )
   {
      height = atoi(argv[2]);
      printf ("%d\n", height);
      if ( height > 5 )
      {
         printf ("You've GOT to be kidding.  ABORT!\n");
         exit(-1);
      }
   }
   else
      scanf ("%d", &height);

   getData (&vector, &size);   // The vector to be sorted.

// Capture time to sequentially sort the idential array
   solo = (long*) calloc ( size, sizeof *solo );
   memcpy (solo, vector, size * sizeof *solo);

   start = wallClock();
   partitionedSort ( vector, size, height, 0);
   middle = wallClock();
   qsort( solo, size, sizeof *solo, compare );
   finish = wallClock();

   if ( validate ( vector, size ) )
      puts ("Sorting succeeds.");
   else
      puts ("SORTING FAILS.");

   printf ("Partitioned:  %3.3f\n", (middle-start) );
   printf (" Sequential:  %3.3f\n", (finish-middle) );
   printf ("   Speed-up:  %3.3f\n", (finish-middle)/(middle-start) );
}

// Return a random integer in the range 0 <= rand < ceiling
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
   {  int  item;
      long save = x[lim-1];
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
 * Partitioned merge logic
 *
 * The working core:  each internal node recurses on this function
 * both for its left side and its right side, as nodes one closer to
 * the leaf level.  It then merges the results into the vector
 *
 * Leaf level nodes just sort the vector.
 */
void partitionedSort ( long *vector, int size, int myHeight, int mySelf )
{  int parent,
       rtChild;
   int nxt;

   parent = mySelf & ~(1<<myHeight);
   nxt = myHeight - 1;
   if ( nxt >= 0 )
      rtChild = mySelf | ( 1 << nxt );

   if ( myHeight > 0 )
   {
      int   left_size  = size / 2,
            right_size = size - left_size;
      long *leftArray  = (long*) calloc (left_size, sizeof *leftArray),
           *rightArray = (long*) calloc (right_size, sizeof *rightArray);
      int   i, j, k;                   // Used in the merge logic

#ifdef DEBUG
      printf ("%d processing at node height %d\n", mySelf, myHeight);
#endif
      memcpy (leftArray, vector, left_size*sizeof *leftArray);
      memcpy (rightArray, vector+left_size, right_size*sizeof *rightArray);

      partitionedSort ( leftArray, left_size, nxt, mySelf );
      partitionedSort ( rightArray, right_size, nxt, rtChild );

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
   else
   {
      qsort( vector, size, sizeof *vector, compare );
#ifdef DEBUG
      printf ("%d sorting at leaf level.\n", mySelf);
#endif
   }
#ifdef DEBUG
   if ( parent != mySelf )
      printf ("%d sends data to %d\n", mySelf, parent);
#endif
}
