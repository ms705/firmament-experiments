#include <stdio.h>

void communicate ( int myHeight, int myRank )
{  int parent = myRank & ~(1 << myHeight);

   if ( myHeight > 0 )
   {  int nxt     = myHeight - 1;
      int rtChild = myRank | ( 1 << nxt );

      printf ("%d sending data to %d\n", myRank, rtChild);
      communicate ( nxt, myRank );
      communicate ( nxt, rtChild );
      printf ("%d getting data from %d\n", myRank, rtChild);
   }
   if ( parent != myRank )
      printf ("%d transmitting to %d\n", myRank, parent);
}

int main ( void )
{  int myHeight = 3, myRank = 0;

   printf ("Building a height %d tree\n", myHeight);
   communicate(myHeight, myRank);
   return 0;
}
