# HOME-RANGE IP AND OBSERVATIONS

This page contains information on 12 different vulnerable machines. Each one is  to be completed within the next year. 356 days. They are accessible through the IP addresses provided, and sit between two subnets. 

# 192.168.56.101 - Debian 10 - "EvilBox: One"

    Nmap scan report for 192.168.56.101
    Host is up (0.0022s latency).
    Not shown: 996 closed tcp ports (reset), 2 filtered tcp ports (no-response)
    Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
    PORT   STATE SERVICE    VERSION
    22/tcp open  tcpwrapped
    | ssh-hostkey: 
    |   2048 44:95:50:0b:e4:73:a1:85:11:ca:10:ec:1c:cb:d4:26 (RSA)
    |   256 27:db:6a:c7:3a:9c:5a:0e:47:ba:8d:81:eb:d6:d6:3c (ECDSA)
    |_  256 e3:07:56:a9:25:63:d4:ce:39:01:c1:9a:d9:fe:de:64 (ED25519)
    80/tcp open  tcpwrapped
    |_http-title: Apache2 Debian Default Page: It works
    |_http-server-header: Apache/2.4.38 (Debian)
    Aggressive OS guesses: 3Com Baseline Switch 2924-SFP or Cisco ESW-520 switch or Allied Telesis AT-8000 series switch (85%), Allied Telesis AT-8000S; Dell PowerConnect 2824, 3448, 5316M, or 5324; Linksys SFE2000P, SRW2024, SRW2048, or SRW224G4; or TP-LINK TL-SL3428 switch (85%), Aruba, Cisco, or Netgear switch (Linux 3.10 or 4.4) (85%), Google Fuchsia (85%), Cisco SG 300-10, Dell PowerConnect 2748, Linksys SLM2024, SLM2048, or SLM224P, or Netgear FS728TP or GS724TP switch (85%), Linksys SRW2000-series or Allied Telesyn AT-8000S switch (85%)
    No exact OS matches for host (test conditions non-ideal).

# 192.168.56.102 - Ubuntu - "Pwn the Tron"

    Nmap scan report for 192.168.56.102
    Host is up (0.0023s latency).
    Not shown: 997 closed tcp ports (reset), 1 filtered tcp port (no-response)
    Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
    PORT   STATE SERVICE    VERSION
    22/tcp open  tcpwrapped
    | ssh-hostkey: 
    |   2048 93:74:34:72:3e:7c:56:0a:f5:d5:a1:4d:6c:94:31:2f (RSA)
    |   256 1f:49:9e:8b:0a:4f:01:cc:e5:a9:2c:28:5a:2c:c1:9e (ECDSA)
    |_  256 05:9f:7a:f1:7b:f7:1f:04:ea:14:d4:5f:f0:0a:8f:54 (ED25519)
    80/tcp open  tcpwrapped
    |_http-title: Revive Cybertron
    |_http-server-header: Apache
    Device type: switch
    Running (JUST GUESSING): Cisco embedded (86%)
    OS CPE: cpe:/h:cisco:css_11501
    Aggressive OS guesses: Cisco CSS 11501 switch (86%)
    No exact OS matches for host (test conditions non-ideal).

# 192.168.56.103 - Ubuntu - "Napping"

    Nmap scan report for 192.168.56.103
    Host is up (0.0021s latency).
    Not shown: 996 closed tcp ports (reset), 2 filtered tcp ports (no-response)
    Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
    PORT   STATE SERVICE    VERSION
    22/tcp open  tcpwrapped
    | ssh-hostkey: 
    |   3072 24:c4:fc:dc:4b:f4:31:a0:ad:0d:20:61:fd:ca:ab:79 (RSA)
    |   256 6f:31:b3:e7:7b:aa:22:a2:a7:80:ef:6d:d2:87:6c:be (ECDSA)
    |_  256 af:01:85:cf:dd:43:e9:8d:32:50:83:b2:41:ec:1d:3b (ED25519)
    80/tcp open  tcpwrapped
    | http-cookie-flags: 
    |   /: 
    |     PHPSESSID: 
    |_      httponly flag not set
    |_http-title: Login
    |_http-server-header: Apache/2.4.41 (Ubuntu)
    Device type: switch
    Running (JUST GUESSING): Cisco embedded (86%)
    OS CPE: cpe:/h:cisco:css_11501
    Aggressive OS guesses: Cisco CSS 11501 switch (86%)
    No exact OS matches for host (test conditions non-ideal).

# 192.168.56.104 - Ubuntu - "Zico's Shop"

    Nmap scan report for 192.168.56.104
    Host is up (0.0021s latency).
    Not shown: 996 closed tcp ports (reset), 1 filtered tcp port (no-response)
    Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
    PORT    STATE SERVICE    VERSION
    22/tcp  open  tcpwrapped
    | ssh-hostkey: 
    |   1024 68:60:de:c2:2b:c6:16:d8:5b:88:be:e3:cc:a1:25:75 (DSA)
    |   2048 50:db:75:ba:11:2f:43:c9:ab:14:40:6d:7f:a1:ee:e3 (RSA)
    |_  256 11:5d:55:29:8a:77:d8:08:b4:00:9b:a3:61:93:fe:e5 (ECDSA)
    80/tcp  open  tcpwrapped
    |_http-server-header: Apache/2.2.22 (Ubuntu)
    |_http-title: Zico's Shop
    111/tcp open  tcpwrapped
    | rpcinfo: 
    |   program version    port/proto  service
    |   100000  2,3,4        111/tcp   rpcbind
    |   100000  2,3,4        111/udp   rpcbind
    |   100000  3,4          111/tcp6  rpcbind
    |   100000  3,4          111/udp6  rpcbind
    |   100024  1          33490/tcp   status
    |   100024  1          38581/tcp6  status
    |   100024  1          39577/udp   status
    |_  100024  1          53533/udp6  status
    Device type: switch|VoIP phone|general purpose
    Running (JUST GUESSING): Cisco embedded (87%), Aastra embedded (86%), Avaya embedded (85%), FreeBSD 4.X (85%)
    OS CPE: cpe:/h:cisco:css_11501 cpe:/h:aastra:57i cpe:/o:freebsd:freebsd:4.7
    Aggressive OS guesses: Cisco CSS 11501 switch (87%), Aastra 57i VoIP phone (86%), Avaya P130 workgroup switch (85%), FreeBSD 4.7-STABLE (85%)
    No exact OS matches for host (test conditions non-ideal).


# 192.168.56.105 - Debian - "symfonos4"
    
    Nmap scan report for 192.168.56.105
    Host is up (0.014s latency).
    Not shown: 998 closed tcp ports (reset)
    PORT   STATE SERVICE    VERSION
    22/tcp open  tcpwrapped
    | ssh-hostkey: 
    |   2048 f9:c1:73:95:a4:17:df:f6:ed:5c:8e:8a:c8:05:f9:8f (RSA)
    |   256 be:c1:fd:f1:33:64:39:9a:68:35:64:f9:bd:27:ec:01 (ECDSA)
    |_  256 66:f7:6a:e8:ed:d5:1d:2d:36:32:64:39:38:4f:9c:8a (ED25519)
    80/tcp open  tcpwrapped
    |_http-server-header: Apache/2.4.38 (Debian)
    |_http-title: Site doesn't have a title (text/html).
    Device type: switch|VoIP phone|general purpose
    Running (JUST GUESSING): Cisco embedded (87%), Aastra embedded (86%), Avaya embedded (85%), FreeBSD 4.X (85%)
    OS CPE: cpe:/h:cisco:css_11501 cpe:/h:aastra:57i cpe:/o:freebsd:freebsd:4.7
    Aggressive OS guesses: Cisco CSS 11501 switch (87%), Aastra 57i VoIP phone (86%), Avaya P130 workgroup switch (85%), FreeBSD 4.7-STABLE (85%)
    No exact OS matches for host (test conditions non-ideal). 

# 192.168.56.106 - Ubuntu - "Web Server:Bootcamp"

    Nmap scan report for 192.168.56.106
    Host is up (0.0025s latency).
    Not shown: 988 closed tcp ports (reset)
    PORT     STATE SERVICE    VERSION
    21/tcp   open  tcpwrapped
    | ftp-syst: 
    |   STAT: 
    | FTP server status:
    |      Connected to 192.168.56.1
    |      Logged in as ftp
    |      TYPE: ASCII
    |      No session bandwidth limit
    |      Session timeout in seconds is 300
    |      Control connection is plain text
    |      Data connections will be plain text
    |      vsFTPd 2.3.4 - secure, fast, stable
    |_End of status
    |_ftp-anon: Anonymous FTP login allowed (FTP code 230)
    22/tcp   open  tcpwrapped
    | ssh-hostkey: 
    |   1024 60:0f:cf:e1:c0:5f:6a:74:d6:90:24:fa:c4:d5:6c:cd (DSA)
    |_  2048 56:56:24:0f:21:1d:de:a7:2b:ae:61:b1:24:3d:e8:f3 (RSA)
    23/tcp   open  tcpwrapped
    25/tcp   open  tcpwrapped
    |_smtp-commands: SMTP EHLO nmap.scanme.org: failed to receive data: connection closed
    53/tcp   open  tcpwrapped
    80/tcp   open  tcpwrapped
    |_http-title: Cybersecurity Bootcamp Server
    111/tcp  open  tcpwrapped
    | rpcinfo: 
    |   program version    port/proto  service
    |   100000  2            111/tcp   rpcbind
    |   100000  2            111/udp   rpcbind
    |   100003  2,3,4       2049/tcp   nfs
    |   100003  2,3,4       2049/udp   nfs
    |   100005  1,2,3      44705/tcp   mountd
    |   100005  1,2,3      48639/udp   mountd
    |   100021  1,3,4      40190/tcp   nlockmgr
    |   100021  1,3,4      56490/udp   nlockmgr
    |   100024  1          43097/tcp   status
    |_  100024  1          54226/udp   status
    139/tcp  open  tcpwrapped
    445/tcp  open  tcpwrapped Samba smbd 3.0.20-Debian
    3306/tcp open  tcpwrapped
    | mysql-info: 
    |   Protocol: 10
    |   Version: 5.0.51a-3ubuntu5
    |   Thread ID: 16
    |   Capabilities flags: 43564
    |   Some Capabilities: LongColumnFlag, Speaks41ProtocolNew, Support41Auth, SwitchToSSLAfterHandshake, ConnectWithDatabase, SupportsTransactions, SupportsCompression
    |   Status: Autocommit
    |_  Salt: EROu~<MN~Sao*}\68Sz0
    5900/tcp open  tcpwrapped
    | vnc-info: 
    |   Protocol version: 3.3
    |   Security types: 
    |_    VNC Authentication (2)
    8180/tcp open  tcpwrapped
    |_http-title: Apache Tomcat/5.5
    Device type: switch|VoIP phone|general purpose
    Running (JUST GUESSING): Cisco embedded (87%), Aastra embedded (86%), Avaya embedded (85%), FreeBSD 4.X (85%)
    OS CPE: cpe:/h:cisco:css_11501 cpe:/h:aastra:57i cpe:/o:freebsd:freebsd:4.7
    Aggressive OS guesses: Cisco CSS 11501 switch (87%), Aastra 57i VoIP phone (86%), Avaya P130 workgroup switch (85%), FreeBSD 4.7-STABLE (85%)
    No exact OS matches for host (test conditions non-ideal).

    Host script results:
    |_smb2-time: Protocol negotiation failed (SMB2)
    | smb-security-mode: 
    |   account_used: guest
    |   authentication_level: user
    |   challenge_response: supported
    |_  message_signing: disabled (dangerous, but default)
    |_clock-skew: mean: 2h00m09s, deviation: 2h50m00s, median: -3s
    | smb-os-discovery: 
    |   OS: Unix (Samba 3.0.20-Debian)
    |   Computer name: webserver
    |   NetBIOS computer name: 
    |   Domain name: localdomain
    |   FQDN: webserver.localdomain
    |_  System time: 2026-06-03T12:51:51-04:00
    |_nbstat: NetBIOS name: WEBSERVER, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)

# 192.168.56.175 - Ubuntu - "Production Server:Bootcamp"

    Nmap scan report for 192.168.56.175
    Host is up (0.0037s latency).
    Not shown: 986 closed tcp ports (reset)
    PORT      STATE SERVICE    VERSION
    21/tcp    open  ftp        vsftpd 2.3.4
    |_ftp-anon: Anonymous FTP login allowed (FTP code 230)
    | ftp-syst: 
    |   STAT: 
    | FTP server status:
    |      Connected to 192.168.56.1
    |      Logged in as ftp
    |      TYPE: ASCII
    |      No session bandwidth limit
    |      Session timeout in seconds is 300
    |      Control connection is plain text
    |      Data connections will be plain text
    |      vsFTPd 2.3.4 - secure, fast, stable
    |_End of status
    22/tcp    open  tcpwrapped
    | ssh-hostkey: 
    |   1024 60:0f:cf:e1:c0:5f:6a:74:d6:90:24:fa:c4:d5:6c:cd (DSA)
    |_  2048 56:56:24:0f:21:1d:de:a7:2b:ae:61:b1:24:3d:e8:f3 (RSA)
    23/tcp    open  tcpwrapped
    25/tcp    open  tcpwrapped
    |_smtp-commands: metasploitable.localdomain, PIPELINING, SIZE 10240000, VRFY, ETRN, STARTTLS, ENHANCEDSTATUSCODES, 8BITMIME, DSN
    53/tcp    open  tcpwrapped
    | dns-nsid: 
    |_  bind.version: 9.4.2
    80/tcp    open  tcpwrapped
    |_http-server-header: Apache/2.2.8 (Ubuntu) DAV/2
    |_http-title: Metasploitable2 - Linux
    111/tcp   open  tcpwrapped
    | rpcinfo: 
    |   program version    port/proto  service
    |   100000  2            111/tcp   rpcbind
    |   100000  2            111/udp   rpcbind
    |   100003  2,3,4       2049/tcp   nfs
    |   100003  2,3,4       2049/udp   nfs
    |   100005  1,2,3      36130/udp   mountd
    |   100005  1,2,3      36975/tcp   mountd
    |   100021  1,3,4      35043/tcp   nlockmgr
    |   100021  1,3,4      48857/udp   nlockmgr
    |   100024  1          36574/tcp   status
    |_  100024  1          42199/udp   status
    139/tcp   open  tcpwrapped
    445/tcp   open  tcpwrapped Samba smbd 3.0.20-Debian
    1524/tcp  open  tcpwrapped
    3306/tcp  open  tcpwrapped
    5900/tcp  open  tcpwrapped
    | vnc-info: 
    |   Protocol version: 3.3
    |   Security types: 
    |_    VNC Authentication (2)
    8180/tcp  open  tcpwrapped
    |_http-favicon: Apache Tomcat
    |_http-title: Apache Tomcat/5.5
    32775/tcp open  tcpwrapped
    OS fingerprint not ideal because: Didn't receive UDP response. Please try again with -sSU
    No OS matches for host
    Service Info: OS: Unix

    Host script results:
    |_clock-skew: mean: 2h00m03s, deviation: 2h49m50s, median: -2s
    | smb-os-discovery: 
    |   OS: Unix (Samba 3.0.20-Debian)
    |   Computer name: metasploitable
    |   NetBIOS computer name: 
    |   Domain name: localdomain
    |   FQDN: metasploitable.localdomain
    |_  System time: 2026-06-03T13:03:03-04:00
    |_smb2-time: Protocol negotiation failed (SMB2)
    | smb-security-mode: 
    |   account_used: <blank>
    |   authentication_level: user
    |   challenge_response: supported
    |_  message_signing: disabled (dangerous, but default)
    |_nbstat: NetBIOS name: METASPLOITABLE, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)

# 10.10.10.2 - Ubuntu - "Metasploitable 2: Completely Open Edition"

This box is pure Metasploitable2, as is, and with everything configurable and accessible. So my inital testing ground for each phase lies here.

    Nmap scan report for 10.10.10.2
    Host is up (0.0052s latency).
    Not shown: 977 closed tcp ports (reset)
    PORT     STATE SERVICE    VERSION
    21/tcp   open  tcpwrapped
    |_ftp-anon: Anonymous FTP login allowed (FTP code 230)
    | ftp-syst: 
    |   STAT: 
    | FTP server status:
    |      Connected to 10.10.10.1
    |      Logged in as ftp
    |      TYPE: ASCII
    |      No session bandwidth limit
    |      Session timeout in seconds is 300
    |      Control connection is plain text
    |      Data connections will be plain text
    |      vsFTPd 2.3.4 - secure, fast, stable
    |_End of status
    22/tcp   open  tcpwrapped
    | ssh-hostkey: 
    |   1024 60:0f:cf:e1:c0:5f:6a:74:d6:90:24:fa:c4:d5:6c:cd (DSA)
    |_  2048 56:56:24:0f:21:1d:de:a7:2b:ae:61:b1:24:3d:e8:f3 (RSA)
    23/tcp   open  tcpwrapped
    25/tcp   open  tcpwrapped
    |_smtp-commands: metasploitable.localdomain, PIPELINING, SIZE 10240000, VRFY, ETRN, STARTTLS, ENHANCEDSTATUSCODES, 8BITMIME, DSN
    53/tcp   open  tcpwrapped
    | dns-nsid: 
    |_  bind.version: 9.4.2
    80/tcp   open  tcpwrapped
    |_http-server-header: Apache/2.2.8 (Ubuntu) DAV/2
    |_http-title: Metasploitable2 - Linux
    111/tcp  open  tcpwrapped
    | rpcinfo: 
    |   program version    port/proto  service
    |   100000  2            111/tcp   rpcbind
    |   100000  2            111/udp   rpcbind
    |   100003  2,3,4       2049/tcp   nfs
    |   100003  2,3,4       2049/udp   nfs
    |   100005  1,2,3      36418/tcp   mountd
    |   100005  1,2,3      59367/udp   mountd
    |   100021  1,3,4      44914/tcp   nlockmgr
    |   100021  1,3,4      60384/udp   nlockmgr
    |   100024  1          44803/udp   status
    |_  100024  1          57885/tcp   status
    139/tcp  open  tcpwrapped
    445/tcp  open  tcpwrapped Samba smbd 3.0.20-Debian
    512/tcp  open  tcpwrapped
    513/tcp  open  tcpwrapped
    514/tcp  open  tcpwrapped
    1099/tcp open  tcpwrapped
    1524/tcp open  tcpwrapped
    2049/tcp open  tcpwrapped
    2121/tcp open  tcpwrapped
    3306/tcp open  tcpwrapped
    | mysql-info: 
    |   Protocol: 10
    |   Version: 5.0.51a-3ubuntu5
    |   Thread ID: 21
    |   Capabilities flags: 43564
    |   Some Capabilities: Support41Auth, SupportsCompression, SwitchToSSLAfterHandshake, LongColumnFlag, Speaks41ProtocolNew, SupportsTransactions, ConnectWithDatabase
    |   Status: Autocommit
    |_  Salt: stj9{$:9Pe-Mz@n-2Q%a
    5432/tcp open  tcpwrapped
    |_ssl-date: 2026-06-03T16:14:19+00:00; 0s from scanner time.
    | ssl-cert: Subject: commonName=ubuntu804-base.localdomain/organizationName=OCOSA/stateOrProvinceName=There is no such thing outside US/countryName=XX
    | Not valid before: 2010-03-17T14:07:45
    |_Not valid after:  2010-04-16T14:07:45
    5900/tcp open  tcpwrapped
    | vnc-info: 
    |   Protocol version: 3.3
    |   Security types: 
    |_    VNC Authentication (2)
    6000/tcp open  tcpwrapped
    6667/tcp open  tcpwrapped
    8009/tcp open  tcpwrapped
    |_ajp-methods: Failed to get a valid response for the OPTION request
    8180/tcp open  tcpwrapped
    |_http-title: Apache Tomcat/5.5
    |_http-favicon: Apache Tomcat
    Aggressive OS guesses: Aastra 57i VoIP phone (95%), Avaya P130 workgroup switch (95%), FreeBSD 4.7-STABLE (95%), Slingmedia Slingbox AV TV over IP gateway (94%), IBM AIX 5.3 (93%), Scientific Atlanta WebSTAR EPC2203 cable modem (92%), Ricoh Aficio MP C4501 printer (91%), Schweitzer Engineering SEL-2701 Ethernet processor (91%), Sony Ericsson P1i mobile phone (Symbian OS 9.1) (90%), Apple iPod touch audio player (iPhone OS 2.2) (90%)
    No exact OS matches for host (test conditions non-ideal).

    Host script results:
    |_nbstat: NetBIOS name: METASPLOITABLE, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
    |_clock-skew: mean: 1h20m01s, deviation: 2h18m37s, median: 0s
    | smb-os-discovery: 
    |   OS: Unix (Samba 3.0.20-Debian)
    |   Computer name: metasploitable
    |   NetBIOS computer name: 
    |   Domain name: localdomain
    |   FQDN: metasploitable.localdomain
    |_  System time: 2026-06-03T12:11:45-04:00
    | smb-security-mode: 
    |   account_used: <blank>
    |   authentication_level: user
    |   challenge_response: supported
    |_  message_signing: disabled (dangerous, but default)
    |_smb2-time: Protocol negotiation failed (SMB2)


# 10.10.10.3 - Debian - "Morpheus:1"

    Nmap scan report for 10.10.10.3
    Host is up (0.0047s latency).
    Not shown: 997 closed tcp ports (reset)
    PORT   STATE SERVICE    VERSION
    22/tcp open  tcpwrapped
    | ssh-hostkey: 
    |_  256 aa:83:c3:51:78:61:70:e5:b7:46:9f:07:c4:ba:31:e4 (ECDSA)
    80/tcp open  tcpwrapped
    |_http-server-header: Apache/2.4.51 (Debian)
    |_http-title: Morpheus:1
    81/tcp open  tcpwrapped
    Aggressive OS guesses: Aastra 57i VoIP phone (96%), Avaya P130 workgroup switch (96%), FreeBSD 4.7-STABLE (96%), Slingmedia Slingbox AV TV over IP gateway (95%), IBM AIX 5.3 (94%), Scientific Atlanta WebSTAR EPC2203 cable modem (93%), Ricoh Aficio MP C4501 printer (92%), Schweitzer Engineering SEL-2701 Ethernet processor (92%), Sony Ericsson P1i mobile phone (Symbian OS 9.1) (91%), Apple iPod touch audio player (iPhone OS 2.2) (91%)
    No exact OS matches for host (test conditions non-ideal).

# 10.10.10.4 - Apache Https server - "Mr. Robot"

    Nmap scan report for 10.10.10.4
    Host is up (0.0033s latency).
    Not shown: 702 closed tcp ports (reset), 296 filtered tcp ports (no-response)
    Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
    PORT    STATE SERVICE        VERSION
    80/tcp  open  tcpwrapped
    |_http-title: Site doesn't have a title (text/html).
    |_http-server-header: Apache
    443/tcp open  ssl/tcpwrapped
    |_ssl-date: TLS randomness does not represent time
    |_http-title: Site doesn't have a title (text/html).
    | ssl-cert: Subject: commonName=www.example.com
    | Not valid before: 2015-09-16T10:45:03
    |_Not valid after:  2025-09-13T10:45:03
    |_http-server-header: Apache
    Aggressive OS guesses: Avaya P130 workgroup switch (92%), FreeBSD 4.7-STABLE (92%), Slingmedia Slingbox AV TV over IP gateway (91%), Aastra 57i VoIP phone (90%), IBM AIX 5.3 (89%), Scientific Atlanta WebSTAR EPC2203 cable modem (88%), Ricoh Aficio MP C4501 printer (88%), Schweitzer Engineering SEL-2701 Ethernet processor (87%), Sony Ericsson P1i mobile phone (Symbian OS 9.1) (87%), D-Link DI-504 or DI-704P broadband router, or DI-524 WAP (86%)
    No exact OS matches for host (test conditions non-ideal).

2
# 10.10.10.6 Fedora Web Server - "Earth"

    Nmap scan report for 10.10.10.6
    Host is up (0.0080s latency).
    Not shown: 957 closed tcp ports (reset), 40 filtered tcp ports (no-response)
    Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
    PORT    STATE SERVICE        VERSION
    22/tcp  open  tcpwrapped
    | ssh-hostkey: 
    |   256 5b:2c:3f:dc:8b:76:e9:21:7b:d0:56:24:df:be:e9:a8 (ECDSA)
    |_  256 b0:3c:72:3b:72:21:26:ce:3a:84:e8:41:ec:c8:f8:41 (ED25519)
    80/tcp  open  tcpwrapped
    |_http-server-header: Apache/2.4.51 (Fedora) OpenSSL/1.1.1l mod_wsgi/4.7.1 Python/3.9
    |_http-title: Bad Request (400)
    443/tcp open  ssl/tcpwrapped
    | tls-alpn: 
    |_  http/1.1
    |_http-server-header: Apache/2.4.51 (Fedora) OpenSSL/1.1.1l mod_wsgi/4.7.1 Python/3.9
    | http-methods: 
    |_  Potentially risky methods: TRACE
    |_http-title: Test Page for the HTTP Server on Fedora
    |_ssl-date: TLS randomness does not represent time
    | ssl-cert: Subject: commonName=earth.local/stateOrProvinceName=Space
    | Subject Alternative Name: DNS:earth.local, DNS:terratest.earth.local
    | Not valid before: 2021-10-12T23:26:31
    |_Not valid after:  2031-10-10T23:26:31
    Aggressive OS guesses: Aastra 57i VoIP phone (96%), Avaya P130 workgroup switch (96%), FreeBSD 4.7-STABLE (96%), Slingmedia Slingbox AV TV over IP gateway (95%), IBM AIX 5.3 (94%), Scientific Atlanta WebSTAR EPC2203 cable modem (93%), Ricoh Aficio MP C4501 printer (92%), Schweitzer Engineering SEL-2701 Ethernet processor (92%), Sony Ericsson P1i mobile phone (Symbian OS 9.1) (91%), Apple iPod touch audio player (iPhone OS 2.2) (91%)
    No exact OS matches for host (test conditions non-ideal).