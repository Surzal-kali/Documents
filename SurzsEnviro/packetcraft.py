import scapy.all as scapy
from scapy.layers.inet import IP, TCP, UDP
from scapy.layers.l2 import Ether, ARP, sendp
from scapy.layers.http import HTTPRequest, HTTPResponse
from scapy.layers.dns import DNS, DNSQR, DNSRR
import random
import string
import time
import cryptography
from scapy.all import sr1, send, sniff, hexdump

#TODO: Add more protocols (e.g., ICMP, FTP, etc.),
# Add support for crafting packets with custom options and flags,
# Implement functionality for sending packets at specific intervals or in bursts,
# Add error handling and validation for input parameters,
# Implement functionality for saving and loading crafted packets,
# Add support for crafting packets with custom payloads (e.g., binary data, files, etc.),
# Implement functionality for analyzing and visualizing captured packets

class PacketCraft:
    def __init__(self, iface=None):
        self.iface = iface

    def create_ip_packet(self, src_ip, dst_ip, payload):
        ip_packet = IP(src=src_ip, dst=dst_ip) / payload
        return ip_packet

    def create_tcp_packet(self, src_ip, dst_ip, src_port, dst_port, payload):
        tcp_packet = IP(src=src_ip, dst=dst_ip) / TCP(sport=src_port, dport=dst_port) / payload
        return tcp_packet

    def create_udp_packet(self, src_ip, dst_ip, src_port, dst_port, payload):
        udp_packet = IP(src=src_ip, dst=dst_ip) / UDP(sport=src_port, dport=dst_port) / payload
        return udp_packet

    def create_http_request(self, method, host, path):
        http_request = HTTPRequest(
            Method=method,
            Host=host,
            Path=path
        )
        return http_request
    
    def create_http_response(self, status_code, reason, body):
        http_response = HTTPResponse(
            Status_Code=status_code,
            Reason=reason,
            Body=body
        )
        return http_response

    def create_dns_query(self, qname):
        dns_query = DNS(rd=1) / DNSQR(qname=qname)
        return dns_query
    
    def create_dns_response(self, qname, rdata):
        dns_response = DNS(
            qr=1,
            aa=1,
            qd=DNSQR(qname=qname),
            an=DNSRR(rrname=qname, rdata=rdata)
        )
        return dns_response
    
    def send_packet(self, packet):
        send(packet, iface=self.iface)

    def sniff_packets(self, filter=None, count=0):
        packets = sniff(filter=filter, count=count, iface=self.iface)
        return packets
    
    def hexdump_packet(self, packet):
        hexdump(packet)
        return hexdump(packet)  