/*
 * Malware Development for Ethical Hackers 2nd
 * victim.c
 * simple "victim" process for injection testing
 * author @cocomelonc
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
  printf("victim process started. PID: %d\n", getpid());

  while (1) {
    printf("hack me... PID: %d\n", getpid());
    sleep(5); // simulate periodic activity
  }

  return 0;
}