/*
 * Malware Development for Ethical Hackers
 * hack.c - Anti-debugging tricks
 * detect debugger
 * author: @cocomelonc
*/

#include <stdio.h>
#include <stdlib.h>
#include <windows.h>

// function to check if a debugger is present
bool IsDebuggerPresentCheck() {
  return IsDebuggerPresent() == TRUE;
}

// function that simulates the main functionality
void hack() {
  MessageBox(NULL, "Meow!", "=^..^=", MB_OK);
}

int main() {
  // check if a debugger is present
  if (IsDebuggerPresentCheck()) {
    MessageBox(NULL, "Debugger detected!", "=^..^=", MB_OK);
    return 1;  // exit if a debugger is present
  }
  // main functionality
  hack();
  return 0;
}
