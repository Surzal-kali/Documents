import sqlite3
from computerspeak import ComputerSpeak as cs
from whatprocess import WhatProcess as wp
from fileshuttle import FileShuttle as fs
from enumeration import FileCrawler as fc
from shellwalking import ShellWalker as sw

### This is an absolute nightmare for me, so i will be putting it off till we crack Marlin. Until then, remember that this is for SQLi-ing databases, similar to sqlmap. but in house :D Please only use for education and testing purposes, and not for any malicious intent. No one wants to be THAT asshole.

def GetDBStatus(database_path):
    """Checks the status of the database and prints out basic information."""
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("[*] Database Tables:")
    for table in tables:
        print(f" - {table[0]}")
    conn.close()
def GetSessions(database_path):
    """Retrieves and prints information about active sessions."""
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("SELECT session_id, host, port, type FROM sessions;")
    sessions = cursor.fetchall()
    print("[*] Active Sessions:")
    for session in sessions:
        print(f" - Session ID: {session[0]}, Host: {session[1]}, Port: {session[2]}, Type: {session[3]}")
    conn.close()