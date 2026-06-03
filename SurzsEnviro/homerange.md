# HOME-RANGE IP AND OBSERVATIONS

This page contains information on 12 different vulnerable machines. Each one is alloted cumutivaly to be completed within the next year. 356 days. They are accessible through the IP addresses provided, and sit between two subnets. 

# 192.168.56.101 - Debian 10 - "EvilBox: One"

    ports open: 22 tcp 7.9p1 and 80 tcp Apache 2.4.38

# 192.168.56.102 - Ubuntu - "Pwn the Tron"

    ports open: 22 tcp 7.6p1 and 80 tcp Apache httpd

# 192.168.56.103 - Ubuntu - "Napping"

    ports open: 22tcp 8.2p1 and 80tcp Apache httpd 2.4.41 (protocol 2.0)

# 192.168.56.104 - Ubuntu - "Zico's Shop"

    ports open: 22 tcp 5.9p1 80 tcp httpd 2.2.22 Apache, 111 udp rpc 2-4, 123 udp NTP v4 (unsychnronized)

# 192.168.56.105 - Debian - "symfonos4"
    
    ports open: 22 tcp 7.9p1 80 tcp http Apache 2.4.38

# 192.168.56.106 - Ubuntu - "Web Server:Bootcamp"

# 192.168.56.175 - Ubuntu - "Production Server:Bootcamp"

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