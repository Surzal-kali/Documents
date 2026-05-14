/*
 * Malware Development for Ethical Hackers
 * hack2.c - Anti-debugging tricks
 * detect debugger via CheckRemoteDebuggerPresent
 * author: @cocomelonc
*/

#include <stdio.h>
#include <stdlib.h>
#include <windows.h>

// function to check if a debugger is present
bool DebuggerCheck() {
  BOOL result;
  CheckRemoteDebuggerPresent(GetCurrentProcess(), &result);
  return result;
}

// function that simulates the main functionality
void hack() {
  MessageBox(NULL, "Meow!", "=^..^=", MB_OK);
}

int main() {
  // check if a debugger is present
  if (DebuggerCheck()) {
    MessageBox(NULL, "Bow-wow!", "=^..^=", MB_OK);
    return 1;  // exit if a debugger is present
  }
  // main functionality
  hack();
  return 0;
}
