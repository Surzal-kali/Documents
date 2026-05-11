import scapy.all as scapy
from scapy.layers.inet import IP, TCP, UDP
from scapy.layers.l2 import Ether
from scapy.layers.http import HTTPRequest, HTTPResponse
from scapy.layers.dns import DNS, DNSQR, DNSRR
import random
import string
import time
import cryptography
from scapy.all import sr1, send, sniff, hexdump

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

    def create_dns_query(self, qname):
        dns_query = DNS(rd=1) / DNSQR(qname=qname)
        return dns_query
    