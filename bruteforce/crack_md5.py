#!/usr/bin/env python3
"""
Fast MD5-crypt ($1$) cracker — wraps john and hashcat as subprocesses.
Phase 1: wordlist attack, Phase 2: brute force with john's rules.
"""

import subprocess
import sys
import os

HASHES_FILE = "/home/surzal/git/cleanpivot/hashest.txt"
WORDLIST = "/home/surzal/git/cleanpivot/rockyou.txt"


def run_cmd(cmd, timeout=None):
    """Run a command and return output."""
    print(f"  Running: {' '.join(cmd[:5])}...")
    result = subprocess.run(
        cmd, capture_output=True, text=True, timeout=timeout
    )
    return result


def crack_with_john_wordlist():
    """Phase 1: john with wordlist."""
    print("\n[=] Phase 1: John wordlist attack...")
    r = run_cmd([
        "john",
        "--wordlist=" + WORDLIST,
        HASHES_FILE
    ])
    if r.returncode == 0 or "loaded" in r.stderr.lower():
        # Check results
        show = run_cmd(["john", "--show", HASHES_FILE])
        if ":" in show.stdout:
            print(show.stdout)
            return True
    return False


def crack_with_john_rules():
    """Phase 2: john with rules for brute force."""
    print("\n[=] Phase 2: John rule-based attack...")
    # best64.rule is aggressive — tries common mutations
    r = run_cmd([
        "john",
        "--wordlist=" + WORDLIST,
        "--rules=JtR-rule:best64",
        HASHES_FILE
    ])
    show = run_cmd(["john", "--show", HASHES_FILE])
    if ":" in show.stdout:
        print(show.stdout)
        return True
    # Try single-key mode (tries username, hostname, etc.)
    print("  Trying single-key mode...")
    r = run_cmd([
        "john",
        "--single",
        HASHES_FILE
    ])
    show = run_cmd(["john", "--show", HASHES_FILE])
    if ":" in show.stdout:
        print(show.stdout)
        return True
    return False


def crack_with_hashcat():
    """Alternative: use hashcat for GPU acceleration."""
    print("\n[=] Phase 1: Hashcat wordlist attack...")
    r = run_cmd([
        "hashcat",
        "-m", "500",
        HASHES_FILE,
        WORDLIST,
        "--force"  # skip warnings
    ])
    # Check for cracked password in output
    if "session" in r.stdout.lower() or "started" in r.stdout.lower():
        # hashcat saves to .potfile
        potfile = "/root/.hashcat/hashcat.potfile"
        if os.path.exists(potfile):
            with open(potfile) as f:
                for line in f:
                    if ":" in line and "$1$" in line:
                        print(f"[+] CRACKED: {line.strip()}")
                        return True
    return False


def main():
    print("[*] Hash file:", HASHES_FILE)
    
    # Verify hash format
    with open(HASHES_FILE) as f:
        for line in f:
            if "$1$" in line:
                print(f"[*] Format: MD5-crypt ($1$)")
                break
    
    # Try john first (CPU, reliable)
    if crack_with_john_wordlist():
        return
    
    if crack_with_john_rules():
        return
    
    # Fallback to hashcat if available
    try:
        subprocess.run(["hashcat", "--version"], capture_output=True)
        if crack_with_hashcat():
            return
    except FileNotFoundError:
        print("[!] hashcat not installed")

    print("\n[-] Could not crack the hash.")
    print("  Try:")
    print("    john --wordlist=rockyou.txt hashes.txt")
    print("    hashcat -m 500 hashes.txt rockyou.txt")


if __name__ == "__main__":
    main()
