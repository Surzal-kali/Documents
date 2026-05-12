import scapy.all as scapy
from scapy.layers.inet import IP, TCP, UDP
from scapy.layers.l2 import Ether, ARP, sendp
from scapy.layers.http import HTTPRequest, HTTPResponse
from scapy.layers.dns import DNS, DNSQR, DNSRR
import random
import string
import time
import cryptography
from scapy.all import sr1, send, sniff, hexdump, Raw
from target_config import TARGET_INTERFACE, TARGET_IP, TARGET_RANGE
#TODO: Add more protocols (e.g., ICMP, FTP, etc.),
# Add support for crafting packets with custom options and flags,
# Implement functionality for sending packets at specific intervals or in bursts,
# Add error handling and validation for input parameters,
# Implement functionality for saving and loading crafted packets,
# Add support for crafting packets with custom payloads (e.g., binary data, files, etc.),
# Implement functionality for analyzing and visualizing captured packets

class PacketCraft:
    def __init__(self, interface: str = TARGET_INTERFACE):
        self.interface = interface

    def craft_tcp_packet(self, src_ip: str, dst_ip: str, src_port: int, dst_port: int, flags: str = "S", payload: bytes = b"") -> scapy.Packet:
        packet = IP(src=src_ip, dst=dst_ip) / TCP(sport=src_port, dport=dst_port, flags=flags) / Raw(load=payload)
        return packet

    def craft_udp_packet(self, src_ip: str, dst_ip: str, src_port: int, dst_port: int, payload: bytes = b"") -> scapy.Packet:
        packet = IP(src=src_ip, dst=dst_ip) / UDP(sport=src_port, dport=dst_port) / Raw(load=payload)
        return packet

    def craft_arp_packet(self, src_mac: str, dst_mac: str, src_ip: str, dst_ip: str) -> scapy.Packet:
        packet = Ether(src=src_mac, dst=dst_mac) / ARP(hwsrc=src_mac, psrc=src_ip, hwdst=dst_mac, pdst=dst_ip)
        return packet
    
    def vlan_frame(self, src_mac: str, dst_mac: str, vlan_id: int, payload: bytes = b"") -> scapy.Packet:
        packet = Ether(src=src_mac, dst=dst_mac) / scapy.Dot1Q(vlan=vlan_id) / Raw(load=payload)
        return packet

    def 