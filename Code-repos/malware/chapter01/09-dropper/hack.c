/*
 * Malware Development for Ethical Hackers
 * hack.c
 * simple DLL
 * author: @cocomelonc
*/
#include <windows.h>

BOOL APIENTRY DllMain(HMODULE moduleHandle, DWORD actionReason, LPVOID reservedPointer) {
  switch (actionReason) {
  case DLL_PROCESS_ATTACH:
    MessageBox(
      NULL,
      "Hello, Packt!",
      "=^..^=",
      MB_OK
    );
    break;
  case DLL_PROCESS_DETACH:
    break;
  case DLL_THREAD_ATTACH:
    break;
  case DLL_THREAD_DETACH:
    break;
  }
  return TRUE;
}
