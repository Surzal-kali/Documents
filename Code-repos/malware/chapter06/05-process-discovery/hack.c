/*
 * Malware Development for Ethical Hackers 2nd
 * hack.c
 * simple pid hunter using /proc/[pid]/comm
 * author: @cocomelonc
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <ctype.h>

int find_process_by_name(const char *proc_name) {
  DIR *dir;
  struct dirent *entry;
  int pid = -1; 

  // open the /proc directory
  dir = opendir("/proc");
  if (dir == NULL) {
    perror("opendir /proc failed"); 
    return -1;
  }

  // iterate through all entries in /proc
  while ((entry = readdir(dir)) != NULL) {
    // skip non-numeric directories (only numeric names are PIDs)
    if (isdigit(*entry->d_name)) { 
      char path[512];
      snprintf(path, sizeof(path), "/proc/%s/comm", entry->d_name); 

      // open the 'comm' file for the current PID
      FILE *fp = fopen(path, "r");
      if (fp) {
        char comm[512];
        if (fgets(comm, sizeof(comm), fp) != NULL) {
          // remove trailing newline characters
          comm[strcspn(comm, "\r\n")] = 0; 
          
          // check if the process name matches our target
          if (strcmp(comm, proc_name) == 0) {
            pid = atoi(entry->d_name); 
            fclose(fp);
            break;
          }
        }
        fclose(fp);
      }
    }
  }

  closedir(dir);
  return pid;
}

int main(int argc, char *argv[]) {
  if (argc != 2) {
    fprintf(stderr, "usage: %s <process_name>\n", argv[0]);
    return 1;
  }

  int pid = find_process_by_name(argv[1]);
  if (pid != -1) {
    printf("found pid - %d for process - %s\n", pid, argv[1]);
  } else {
    printf("process '%s' not found.\n", argv[1]);
  }

  return 0;
}