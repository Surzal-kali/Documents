Based on your lab environment, homework deadline, and the provided nmap output 
2026-06-12
, here is a clear breakdown of your operational constraints:

1. Environmental & Technical Constraints
Immutable Target State: You cannot patch, restart, or reconfigure any services beyond initial VM integration. Exploitation must work against the live, unaltered configuration.
Fragile Network Stack: The web server crashes under aggressive scanning. All enumeration and exploitation must use low-rate, stateless, or single-packet techniques to avoid triggering DoS conditions.
VNC Port 5900 Exclusion: As identified, port 5900 is bound to VirtualBox's host management layer, not the guest OS network stack. It cannot be used for application-level exploitation.
Guest/Default-Only Auth Model: You must rely strictly on default credentials, anonymous access, or hardcoded backdoors. Custom user creation, password spraying, or brute-forcing is not viable within your constraints.
2. Exploitation & Attack Surface Constraints (From Scan Data 
2026-06-12)
vsftpd 2.3.4 (Port 21) exposes a hardcoded backdoor that triggers upon specific authentication strings without requiring valid credentials 
2026-06-12
.
Apache Tomcat/5.5 (Port 8180) runs the manager application, which historically ships with default deploy credentials allowing direct JSP/WAR uploads if not rotated.
MySQL 5.0.51a & PostgreSQL 8.3.0 disclose precise version banners 
2026-06-12
, but require empty or default passwords to pivot without authentication.
Samba (Ports 139/445) shows disabled message signing by default 
2026-06-12
, which can be leveraged for authentication bypass or relay attacks, but requires careful client-side configuration to avoid triggering host-based alerts.
3. Operational & Timeline Constraints
48-Hour Deadline: Requires sequential, low-friction exploitation chains that produce immediate, recordable proof (terminal output + service banners).
Deliverable Requirements: Must document exactly 4 vulnerabilities, 2 active exploits, and 1 reliable one-shot chain. All proofs must be screenshot/video-ready without installing additional tooling on the targets.
Static Service Map: Since you cannot modify the VMs, any closed ports are permanently inaccessible for this assignment. You must work strictly within the verified open services 
2026-06-12.
4. Ethical & Academic Integrity Constraints
No External Assistance: All work must be completed independently without consulting peers, instructors, or online resources (hence LOCAL BABY).
HAHA no. sorry. i have to right a backdoor for both and PROVE it and i get bonus points for john. 

ALL LOGIC STAYS IN THIS CONTAINER AND INSTANCE. the lan is suitable enough and NOTHING else. 

Documents: https://www.quickstart.com/my-dashboard/#/bootcamp-fileshare 


CVE MANIFEST FOR PRODUCTION SERVER

Description
vsftpd 2.3.4 downloaded between 20110630 and 20110703 contains a backdoor which opens a shell on port 6200/tcp.

http://packetstormsecurity.com/files/162145/vsftpd-2.3.4-Backdoor-Command-Execution.html


# Exploit Title: vsftpd 2.3.4 - Backdoor Command Execution
# Date: 9-04-2021
# Exploit Author: HerculesRD
# Software Link: http://www.linuxfromscratch.org/~thomasp/blfs-book-xsl/server/vsftpd.html
# Version: vsftpd 2.3.4
# Tested on: debian
# CVE : CVE-2011-2523
unix/ftp/vsftpd_234_backdoor <- correct architecture and platform for this exploitse>
msf > use exploit/unix/ftp/vsftpd_234_backdoor
    msf exploit(vsftpd_234_backdoor) > show targets
        ...targets...
    msf exploit(vsftpd_234_backdoor) > set TARGET < target-id >
    msf exploit(vsftpd_234_backdoor) > show options
        ...show and set options... < this is the part i suck at with complex networks> #note: i still need to catch up on a month of network admin. (bit of a struggle ngl)
    msf exploit(vsftpd_234_backdoor) > exploit
    ...exploit output...




https://packetstormsecurity.com/files/102745/VSFTPD-2.3.4-Backdoor-Command-Execution.html




ok so given the exploit won't work because of how the network is configured, I will have to write my own backdoor and then prove it works. so we abuse tailscale serve within the tailnet.

SRV_PORT and LHOST don't really resolve, at least in my head, given the current document, can you draft a prompt with the next steps for me to write a custom backdoor that can be used within the constraints of the lab environment, specifically leveraging Tailscale's serve functionality?Certainly! Below is a prompt that outlines the next steps for writing a custom backdoor that can be used within the constraints of your lab environment, leveraging Tailscale's serve functionality.


### Prompt: Writing a Custom Backdoor Using Tailscale's Serve Functionality

#### Objective:
To create a custom backdoor that can be used within the constraints of the lab environment, specifically leveraging Tailscale's serve functionality to establish a connection back to your local machine.
#### Steps:
1. **Understand Tailscale's Serve Functionality**:
   - Familiarize yourself with Tailscale's serve functionality, which allows you to expose a local service to the Tailscale network. This will be crucial for creating a backdoor that can communicate with your local machine.
   - Review the Tailscale documentation on how to set up and use the serve functionality:
   - [Tailscale Serve Documentation](https://tailscale.com/kb/1017/serve/) (also double check my current subnet routing cause i have 4 routes D:)
 - [Tailscale CLI Reference](https://tailscale.com/kb/1017/serve/#cli-reference)
