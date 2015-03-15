/*
UNIX time value:   number of seconds since 00:00:00 on January 1, 1970 (GMT)).

This is based on information provided by Dr. Richard Sevenich.
*/

#include <sys/time.h>

double wallClock(void)
{
   struct timeval tv;
   double current;

   gettimeofday(&tv, NULL);   // Omit the timezone struct
   current = tv.tv_sec + 1.0e-06 * tv.tv_usec;

   return current;
}
