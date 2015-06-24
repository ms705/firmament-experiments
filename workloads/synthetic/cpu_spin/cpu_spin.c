#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <sys/time.h>
#include <signal.h>

volatile sig_atomic_t flag = 1;

void catch_timer(int sig) {
  flag = 0;
}

int main(int argc, char* argv[]) {
  // One argument: number of seconds to spin for
  char* duration_env = getenv("DURATION");
  int64_t secs;
  if (!duration_env && argc < 2) {
    printf("usage: cpu_spin <seconds>\n");
    exit(1);
  } else if (argc >= 2) {
    secs = atol(argv[1]);
  } else {
    secs = atol(duration_env);
  }
  printf("Spinning for %jds.\n", secs);

  // Set up a timer
  struct itimerval timer;
  timer.it_interval.tv_sec = 0;
  timer.it_interval.tv_usec = 0;
  timer.it_value.tv_sec = secs;
  timer.it_value.tv_usec = 0;

  if (signal(SIGALRM, catch_timer)) return -1;

  if (setitimer(ITIMER_REAL, &timer, NULL)) return -1;

  while (flag) { }

  printf("Spin done.\n");
  return 0;
}
