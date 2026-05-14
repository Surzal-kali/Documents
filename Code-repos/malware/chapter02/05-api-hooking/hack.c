/*
 * Malware Development for Ethical Hackers
 * hack.c
 * illustration of basic hooking technique
 * author: @cocomelonc
*/
#include <windows.h>
#include <stdio.h>

// typedef for the original function signature
typedef int (__cdecl *OriginalCatFunction)(LPCTSTR message);

// define patch size based on architecture
#ifdef _M_X64
  #define PATCH_SIZE 14
#else
  #define PATCH_SIZE 5
#endif

BYTE originalBytes[PATCH_SIZE];
FARPROC hookedFunctionAddress;

// modified Cat function
int __cdecl myModifiedCatFunction(LPCTSTR message) {
  printf("hooked! original message was: %s\n", message);
    
  // first, we remove the hook (restore bytes) to call the original
  WriteProcessMemory(GetCurrentProcess(), (LPVOID)hookedFunctionAddress, originalBytes, PATCH_SIZE, NULL);
    
  // we call the original
  OriginalCatFunction originalCatFunc = (OriginalCatFunction)hookedFunctionAddress;
  int result = originalCatFunc("meow-squeak-tweet!!!");
    
  // put the hook back (optional)
  // installMyHook(); 
  return result;
}

void installMyHook() {
  HMODULE hLib = LoadLibraryA("pet.dll");
  hookedFunctionAddress = GetProcAddress(hLib, "Cat");

  // preserving the original bytes
  ReadProcessMemory(GetCurrentProcess(), (LPCVOID)hookedFunctionAddress, originalBytes, PATCH_SIZE, NULL);

  BYTE patch[PATCH_SIZE] = {0};

#ifdef _M_IX86
  // --- x86 logic (5 byte) ---
  DWORD destination = (DWORD)&myModifiedCatFunction;
  DWORD source = (DWORD)hookedFunctionAddress + 5;
  DWORD relativeOffset = destination - source;

  patch[0] = 0xE9; // JMP rel32
  memcpy(patch + 1, &relativeOffset, 4);

#elif defined(_M_X64)
  // --- x64 logic (14 byte) ---
  // jmp qword ptr [rip + 0] -> FF 25 00 00 00 00
  // this is followed by 8 bytes of absolute address
  patch[0] = 0xFF;
  patch[1] = 0x25;
  // patch[2...5] already 0, 
  // which means "offset 0 from the end of this instruction"
  UINT_PTR destination = (UINT_PTR)&myModifiedCatFunction;
  memcpy(patch + 6, &destination, 8);
#endif

  // patching
  // although WriteProcessMemory temporarily changes protection
  // it is better to explicitly use VirtualProtect
  DWORD oldProtect;
  VirtualProtect((LPVOID)hookedFunctionAddress, PATCH_SIZE, PAGE_EXECUTE_READWRITE, &oldProtect);
  WriteProcessMemory(GetCurrentProcess(), (LPVOID)hookedFunctionAddress, patch, PATCH_SIZE, NULL);
  VirtualProtect((LPVOID)hookedFunctionAddress, PATCH_SIZE, oldProtect, &oldProtect);
}

int main() {
  HINSTANCE petDll;
  OriginalCatFunction originalCatFunc;

  // Load the target DLL
  petDll = LoadLibrary("pet.dll");
  if (petDll == NULL) return -1;
    
  // Obtain the address of the target function
  originalCatFunc = (OriginalCatFunction)GetProcAddress(petDll, "Cat");

  // Call the original function (before hooking)
  printf("original:\n");
  (originalCatFunc)("meow-meow");

  // Install the hook
  installMyHook();

  // Call the function after installing the hook
  // Execution will now flow into myModifiedCatFunction
  printf("after hook:\n");
  (originalCatFunc)("meow-meow");

  // Cleanup
  FreeLibrary(petDll);
  return 0;
}