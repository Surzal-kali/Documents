/*
 * Malware Development for Ethical Hackers 2nd
 * hack.c - simple "malware" for demo
 * author: @cocomelonc
 */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main() {
  char *home = getenv("HOME");
  char path[512];
  sprintf(path, "%s/meow.txt", home);
  const char *hello = "Malware Development for Ethical Hackers by Packt\n";
  FILE *f = fopen(path, "a+");
  if (f) {
    fputs(hello, f);
    fclose(f);
  }
  printf(hello);
  return 0;
}