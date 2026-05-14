/*
 * Malware Development for Ethical Hackers 2nd
 * hack2.c
 * robust multi-target discovery 
 * using /proc/[pid]/cmdline
 * author: @cocomelonc
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <ctype.h>

void find_all_pids_by_name(const char *proc_name) {
  DIR *dir;
  struct dirent *entry;
  int found = 0;

  dir = opendir("/proc");
  if (dir == NULL) {
    perror("opendir /proc failed");
    return;
  }

  while ((entry = readdir(dir)) != NULL) {
    if (isdigit(*entry->d_name)) {
      char path[512];
      snprintf(path, sizeof(path), "/proc/%s/cmdline", entry->d_name);

      FILE *fp = fopen(path, "r");
      if (fp) {
        char cmdline[512];
        if (fgets(cmdline, sizeof(cmdline), fp) != NULL) {
          // cmdline separates args with null bytes. we only need the first arg (binary name)
          cmdline[strcspn(cmdline, "\0")] = 0;

          // strip path: find the last slash to get just the filename
          const char *base_name = strrchr(cmdline, '/');
          base_name = (base_name) ? base_name + 1 : cmdline;

          // use strcasecmp for case-insensitive matching and strstr for substrings
          if (strcasecmp(base_name, proc_name) == 0 || strstr(base_name, proc_name)) {
            printf("found match: %s (PID: %s)\n", base_name, entry->d_name);
            found = 1;
          }
        }
        fclose(fp);
      }
    }
  }

  if (!found) {
    printf("no processes matched the name '%s'.\n", proc_name);
  }

  closedir(dir);
}

int main(int argc, char *argv[]) {
  if (argc != 2) {
    fprintf(stderr, "usage: %s <search_string>\n", argv[0]);
    return 1;
  }

  printf("searching for '%s'...\n", argv[1]);
  find_all_pids_by_name(argv[1]);

  return 0;
}