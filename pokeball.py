import catchingshells
from target_config import TARGET_IP, TARGET_INTERFACE, SELF_IP_RE, TARGET_RANGE
import socket
import os
import subprocess
import sys


#time to write a pokeball throw in malware form. Matrix and Marvin, I choose you!

def main():
    print("[*] Starting pokeball...")
    catchingshells.main(TARGET_IP)