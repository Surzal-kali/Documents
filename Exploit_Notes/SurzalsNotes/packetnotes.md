| Layer | Packet Type | Protocols / Examples | Notes |
| --- | --- | --- | --- |
| Data Link | Ethernet Frames | Ether | The foundation for local network packets. |
| Data Link | ARP Packets | ARP requests/replies | Resolves IP addresses to MAC addresses. |
| Data Link | Wi-Fi Frames | 802.11 management, control, and data frames | Includes Beacon, Probe Request, and RTS/CTS. |
| Internet / Network | IP Packets | IPv4, IPv6 | Provides logical addressing across networks. |
| Internet / Network | Diagnostic Packets | ICMP | Used for error reporting and diagnostics like ping. |
| Transport | TCP Segments | TCP | Connection-oriented and reliable; uses SYN, ACK, FIN, and RST flags. |
| Transport | UDP Datagrams | UDP | Connectionless and fast; common for DNS and streaming. |
| Application | Application Data | HTTP, DNS, and similar protocols | Built on TCP or UDP; Scapy often treats this as payload data. |
| Specialized | RTCP | RTP control traffic | Control protocol for RTP streams. |
| Specialized | DHCP | DHCP | Used for dynamic IP address assignment. |
| Data Link | VLAN-tagged Frames | 802.1Q | Common on switched networks and trunk links. |
| Data Link | Discovery Protocol Packets | LLDP, CDP | Helps identify devices and map network topology. |
| Internet / Network | Neighbor Discovery Packets | NDP, ICMPv6 | IPv6 replacement for ARP. |
| Internet / Network | Routing Protocol Packets | OSPF, BGP, RIP, EIGRP | Used by routers to exchange route information. |
| Internet / Network | Multicast Management Packets | IGMP, MLD | Manages multicast group membership. |
| Transport | SCTP Chunks | SCTP | Less common transport protocol used in signaling and telecom. |
| Specialized | IPsec Packets | AH, ESP | Provides authentication and encryption at the IP layer. |
| Specialized | Tunnel / VPN Packets | GRE, WireGuard, OpenVPN, L2TP, VXLAN | Common in enterprise, cloud, and lab environments. |
| Application | Service Discovery Packets | mDNS, SSDP, NBNS, LLMNR | Frequently appears during local discovery and enumeration. |
| Application | Management / Control Packets | SNMP, NTP, SSH, TLS handshake | Useful for identifying management and encrypted sessions. |
| Specialized | RTP | Real-time Transport Protocol | Carries the media stream that RTCP monitors and controls. |
