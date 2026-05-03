from computerspeak import ComputerSpeak as cs
from pymetasploit3.msfrpc import MsfRpcClient
from metasploiting import search_modules, execute_module, list_sessions, get_db_status, payload_generation
from netrunning import NetRunning as nr
from whatprocess import WhatProcess as wp
from fileshuttle import FileShuttle as fs
from enumeration import FileCrawler as fc
from shellwalking import ShellWalker as sw
from catchingpackets import PacketSniffer as ps
from target_config import MSF_PASS, TARGET_IP, TARGET_INTERFACE, TARGET_USERNAME, TARGET_PASSWORD, TARGET_RANGE, SELF_IP_RE, IPV4_RE, WORDLIST_PATH
from conquer import Tenfold as tf
from orchestrator import Orchestrator as Or
from dacore import CoreClass as cc
import re
import time
from publicface import publicface as Pf

def somerandomcode1():
    pfi = Pf()
    cci = cc()
    psi = ps()
    swi = sw()
    fci = fc()
    wpi = wp()
    nri = nr()
    csi = cs()
    tfi = tf()
    ori = Or()
    print("[*] Welcome Home")

    capture=psi.start_sniffing(1000, 600, f"ip.addr == {TARGET_IP} and tcp.port == 80", "http_traffic.pcap")
    psi.analyze_capture("http_traffic.pcap", "http_traffic.txt")
    http_traffic = psi.parse_http_traffic("http_traffic.txt")
    for request in http_traffic:
        print(f"[*] HTTP Request: {request['method']} {request['url']}")
        print(f"[*] Headers: {request['headers']}")
        print(f"[*] Body: {request['body']}")
        print("-" * 50)



if __name__ == "__main__":  
    somerandomcode1()
    fsi = fs()
    cleanup = input("[*] Do you want to clean up old files from previous runs? (y/n): ")
    if cleanup.lower() == "y":
        fsi.delete_file("bin.txt")
        fsi.delete_file("rawbin.txt")
        print("[*] Old files cleaned up.")