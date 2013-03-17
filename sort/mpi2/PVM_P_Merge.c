/**
 * Exercise a limited-depth-tree parallel merge sort under PVM.
 *
 * Each internal node of the processing tree spawns a single task
 * to handle the processing of the right half of the array it has
 * received.  The left half is handled by the process itself through
 * a recursive call for processing in the next lower level of the
 * processing tree.  Since some function calls will come from nodes
 * that need to return their completed results (that is, dealing
 * with the right side) while others (those dealing with the left
 * side) transform the array in-place, the function receives as a
 * parameter a boolean indicating whether it needs to send a message
 * to its parent with the sorted results.
 *
 * Author:  Timothy Rolfe
 */
#include <stdio.h>
#include <stdlib.h>     // for rand, etc.
#include <time.h>       // for time(NULL)
#include <pvm3.h>
#include "wallClock.c"  // apologies for including source code

//#define  DEBUG

#define  INIT  1        // Message giving size and height
//efine  DATA  2        // Message giving vector to sort
#define  ANSW  3        // Message returning sorted vector
#define  NODE "PVM_P_Merge"

typedef enum { FALSE, TRUE } BOOLEAN;

// Required by qsort()
int compare ( const void* left, const void* right );  // for qsort()

// Parallel merge logic under PVM
void parallelMerge ( long *vector, int size, int myHeight, BOOLEAN report );

// Generate a vector of random data for a size.  Modify the
// variables vector and size by writing through the pointers
// passed (i.e., pointer to long* and pointer to int).
void getData ( long **vPtr, int *sizePtr );

// Verify the array:  for all k, x[k] = k+1
int  validate ( long *vector, int size );

int main ( int argc, char* argv[] )
{
   int   myTid  = pvm_mytid(),
         parent = pvm_parent();
   int   rc;
   int   size = 0;      // Size of the vector being sorted
   long  *vector,        // Vector for parallel sort
         *solo;          // Copy for sequential sort
   double start,        // Begin parallel sort
          middle,       // Finish parallel sort
          finish;       // Finish sequential sort

   srand(time(NULL));// Set up for shuffling

   if ( myTid < 0 )
   {
      puts ("Failed to enroll in PVM.  Abort!");
      exit(-1);
   }

   if ( argc > 1 )
      size = atoi(argv[1]);

   if ( parent == PvmNoParent )   // Host process
   {
      int rootHt;

      fputs ("Height of root:  ", stdout);
      if ( argc > 2 )
      {
         rootHt = atoi(argv[2]);
    printf ("%d\n", rootHt);
      }
      else
         scanf ("%d", &rootHt);

      getData (&vector, &size);   // The vector to be sorted.

   // Capture time to sequentially sort the idential array
      solo = (long*) calloc ( size, sizeof *solo );
      memcpy (solo, vector, size * sizeof *solo);

      start = wallClock();
      parallelMerge ( vector, size, rootHt, FALSE );
      middle = wallClock();
   }
   else                      // Node process
   {
      int   iVect[2],        // Message sent as an array
            height;          // Pulled from iVect

#ifdef DEBUG
      printf ("%#x spawned by %#x\n", myTid, parent);
#endif
      rc = pvm_recv(parent, INIT);
      pvm_upkint ( &size, 1, 1 );
      pvm_upkint ( &height, 1, 1 );
      vector = (long*) calloc (size, sizeof *vector);

      pvm_upklong ( vector, size, 1 );

      parallelMerge ( vector, size, height, TRUE );

      pvm_exit();
      return 0;
   }
// Only the rank-0 process executes here.

   qsort( solo, size, sizeof *solo, compare );

   finish = wallClock();

   pvm_exit();
   if ( validate ( vector, size ) )
      puts ("Sorting succeeds.");
   else
      puts ("SORTING FAILS.");

   printf ("  Parallel:  %3.3f\n", (middle-start) );
   printf ("Sequential:  %3.3f\n", (finish-middle) );
   printf ("  Speed-up:  %3.3f\n", (finish-middle)/(middle-start) );
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
 * Parallel merge logic under PVM
 *
 * The working core:  each internal node ships its right-hand
 * side to the process it spawns to as a node one closer to
 * the leaf level in the processing tree, and then recurses on
 * this function to process the left-hand side as the node one
 * closer to the leaf level.
 *
 * Note:  "report" will be TRUE if this is a right-hand side
 * being processed --- it needs to be sent as a message back to
 * its parent.  If it is a left-hand side, the result is handled
 * automatically because the result is generated in place.
 */
void parallelMerge ( long *vector, int size, int myHeight, BOOLEAN report )
{
   int   myTid  = pvm_mytid(),
         parent = pvm_parent();
   int rc, nxt, rtChild;

   nxt = myHeight - 1;

   if ( myHeight > 0 )
   {
      int   left_size  = size / 2,
            right_size = size - left_size;
      long *leftArray  = (long*) calloc (left_size, sizeof *leftArray),
           *rightArray = (long*) calloc (right_size, sizeof *rightArray);
      int   iVect[2];
      int   i, j, k;                   // Used in the merge logic

      rc = pvm_spawn ( NODE, NULL, 0, "", 1, &rtChild );
#ifdef DEBUG
      printf ("%#x has spawned %#x\n", myTid, rtChild);
#endif
      memcpy (leftArray, vector, left_size*sizeof *leftArray);
      memcpy (rightArray, vector+left_size, right_size*sizeof *rightArray);

      pvm_initsend(PvmDataRaw);
      pvm_pkint ( &right_size, 1, 1 );
      pvm_pkint ( &nxt, 1, 1 );
      pvm_pklong( rightArray, right_size, 1 );
      pvm_send ( rtChild, INIT );

      parallelMerge ( leftArray, left_size, nxt, FALSE );
#ifdef DEBUG
      printf ("%#x waiting for data from %#x\n", myTid, rtChild); fflush(stdout);
#endif
      pvm_recv ( rtChild, ANSW );
      pvm_upklong ( rightArray, right_size, 1 );

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
      printf ("%#x leaf sorting.\n", myTid); fflush(stdout);
#endif
   }

   if ( report )
   {
      pvm_initsend(PvmDataRaw);
      pvm_pklong ( vector, size, 1 );
      pvm_send ( parent, ANSW );
#ifdef DEBUG
      printf ("%#x sending data to %#x\n", myTid, parent);
#endif
   }
}
