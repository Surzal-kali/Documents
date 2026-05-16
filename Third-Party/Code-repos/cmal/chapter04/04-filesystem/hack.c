/*
 * Malware Development for Ethical Hackers
 * hack.c - Anti-VM tricks
 * check filesystem
 * author: @cocomelonc
*/
#include <windows.h>
#include <stdio.h>

BOOL checkVM() {
  // paths to check
  // LPCSTR path1 = "c:\\windows\\system32\\drivers\\VBoxMouse.sys";
  // LPCSTR path2 = "c:\\windows\\system32\\drivers\\VBoxGuest.sys";

  LPCSTR path1 = "c:\\windows\\system32\\drivers\\viofs.sys";
  LPCSTR path2 = "c:\\windows\\system32\\drivers\\vioser.sys";

  // use GetFileAttributes to check if the first file exists
  DWORD attributes1 = GetFileAttributes(path1);

  // use GetFileAttributes to check if the second file exists
  DWORD attributes2 = GetFileAttributes(path2);

  // check if both files exist
  if ((attributes1 != INVALID_FILE_ATTRIBUTES && !(attributes1 & FILE_ATTRIBUTE_DIRECTORY)) ||
    (attributes2 != INVALID_FILE_ATTRIBUTES && !(attributes2 & FILE_ATTRIBUTE_DIRECTORY))) {
    // at least one of the files exists
    return TRUE;
  } else {
    // both files do not exist or are directories
    return FALSE;
  }
}

int main() {
  if (checkVM()) {
    printf("The system appears to be a virtual machine.\n");
  } else {
    printf("The system does not appear to be a virtual machine.\n");
    printf("hacking...");
  }

  return 0;
}
