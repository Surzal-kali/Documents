# Scapy Quick Cheat Sheet

> Practical Scapy reference for packet crafting, fuzzing, and lab automation.  
> Scope: L2-L7 essentials with minimal theory.

---

## Import

```python
from scapy.all import *
```

## Ether / IP / TCP / Raw

### Layer 2

#### Ethernet

```python
Ether(src="00:11:22:33:44:55", dst="ff:ff:ff:ff:ff:ff")
```

#### VLAN (802.1Q)

```python
Ether() / Dot1Q(vlan=10) / IP()
```

#### ARP

```python
Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst="192.168.1.1")
```

### Layer 3

#### IPv4 / IPv6

```python
IP(src="10.0.0.1", dst="8.8.8.8", ttl=64)
IPv6(src="fe80::1", dst="ff02::1")
```

#### ICMP

```python
ICMP(type=8)   # Echo Request
ICMP(type=0)   # Echo Reply
```

### Layer 4

#### TCP

```python
TCP(sport=1234, dport=80, flags="S", seq=100)
```

**Flags:** `S A F R P U`

#### UDP

```python
UDP(sport=53, dport=5353)
```

#### SCTP

```python
SCTP(sport=5000, dport=5000) / SCTPChunkInit()
```

## Payload / Application

### Raw Data

```python
Raw(load=b"hello world")
```

### DNS

```python
DNS(rd=1, qd=DNSQR(qname="example.com"))
```

### DHCP Discover

```python
Ether(dst="ff:ff:ff:ff:ff:ff") \
    / IP(src="0.0.0.0", dst="255.255.255.255") \
    / UDP(sport=68, dport=67) \
    / BOOTP() \
    / DHCP(options=[("message-type", "discover"), "end"])
```

## Multicast / Discovery

### mDNS

```python
IP(dst="224.0.0.251") / UDP(dport=5353) / DNS(qd=DNSQR(qname="_http._tcp.local"))
```

### IGMP

```python
IP(dst="224.0.0.1") / IGMP(type=0x11)
```

## Wireless (802.11)

```python
RadioTap() / Dot11(
    type=0,
    subtype=8,
    addr1="ff:ff:ff:ff:ff:ff",
    addr2="00:11:22:33:44:55",
    addr3="00:11:22:33:44:55",
) / Dot11Beacon() / Dot11Elt(ID="SSID", info="TestNet")
```

## Tunneling / VPN

### GRE

```python
IP(dst="1.2.3.4") / GRE() / IP(dst="10.0.0.2") / TCP()
```

### IPsec (ESP structure)

```python
IP() / ESP(spi=0xDEADBEEF, seq=1)
```

## Sending & Sniffing

### Send

```python
send(pkt)
sendp(pkt, iface="eth0")
```

### Sniff

```python
sniff(filter="udp", count=10)
sniff(prn=lambda p: p.summary())
```

## Inspection

```python
pkt.show()
pkt.summary()
hexdump(pkt)
ls(TCP)
```

## Fuzzing Helpers

```python
RandIP()
RandMAC()
RandShort()
RandNum(1, 65535)
RandString(128)
```

### Example

```python
IP(dst=RandIP()) / UDP(dport=RandShort()) / Raw(load=RandString(256))
```


### Basic Rhythm:

| Time | What dominates |
|------|-----------------|
| 00:00–06:00 | Background + telemetry |
| 06:00–08:30 | Background + app warming |
| 08:30–12:00 | Web + app + admin |
| 12:00–13:00 | Reduced web, app steady |
| 13:00–17:30 | Web + app peak |
| 17:30–22:00 | App + telemetry |
| 22:00–00:00 | Mostly background |
