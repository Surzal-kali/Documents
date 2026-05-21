import socket
import time
from computerspeak import ComputerSpeak as cs
from metasploiting import search_modules, execute_module, list_sessions, get_db_status, payload_generation
from pymetasploit3.msfrpc import MsfRpcClient as Msf
from netrunning import NetRunning as nr
from whatprocess import WhatProcess as wp
from enumeration import FileCrawler as fc
from shellwalking import ShellWalker as sw
from catchingpackets import PacketSniffer as ps
from target_config import MSF_PASS, TARGET_IP, TARGET_INTERFACE, TARGET_USERNAME, TARGET_PASSWORD, TARGET_RANGE, SELF_IP_RE, IPV4_RE, WORDLIST_PATH
from payloads.WIP.conquer import Tenfold as tf
import requests 
import platform

class publicface:
    """This class is designed to be the main entry point for web requests, providing a public-facing interface for various functionalities of web hunting in SurzsEnviro. It can be used for testing, demonstrations, or as a simple interface for users to interact with the underlying tools and modules."""
    #note to self, need to do more research on this with requests, maybe beautiful soup?
    
    def __init__(self):
        self.nri=nr()
        self.fci=fc()
        self.wpi=wp()
        self.csi=cs()
        self.swi=sw()
        self.psi=ps()
        self.tfi=tf()
        self.msfi=Msf(password=MSF_PASS, port=55552, ssl=False)

    @staticmethod
    def hostname_to_ip(hostname):
        try:
            ip_address = socket.gethostbyname(hostname)
            return ip_address
        except socket.gaierror:
            return None

    @staticmethod
    def ip_to_hostname(ip_address):
        try:
            hostname = socket.gethostbyaddr(ip_address)[0]
            return hostname
        except socket.herror:
            return None
    
    @staticmethod
    def get_request(url, headers=None):
        """Make a GET request to the specified URL and return the response content."""
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while making the GET request: {e}")
            return None
    @staticmethod
    def trace_route(url):
        """Trace the route to the specified URL and return the results."""
        csi = cs()
        csi.speak(f"Tracing route to {url}...")
        command = f"tracert {url}" if platform.system() == "Windows" else f"traceroute {url}"
        result = csi.ec(command)
        if result:
            return result
        else:
            return "Failed to trace route."
        
    @staticmethod
    def put_request(url, data, headers=None):
        """Make a PUT request to the specified URL with the given data and return the response content."""
        try:
            response = requests.put(url, data=data, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while making the PUT request: {e}")
            return None
        
    @staticmethod
    def delete_request(url, data=None):
        """Make a DELETE request to the specified URL and return the response content."""
        try:
            response = requests.delete(url, data=data)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while making the DELETE request: {e}")
            return None
    
    @staticmethod
    def post_request(url, data, headers=None):
        """Make a POST request to the specified URL with the given data and return the response content."""
        try:
            response = requests.post(url, data=data, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while making the POST request: {e}")
            return None
    
    @staticmethod
    def head_request(url, headers=None):
        """Make a HEAD request to the specified URL and return the response headers."""
        try:
            response = requests.head(url, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.headers
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while making the HEAD request: {e}")
            return None

    @staticmethod
    def patch_request(url, data, headers=None):
        """Make a PATCH request to the specified URL with the given data and return the response content."""
        try:
            response = requests.patch(url, data=data, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while making the PATCH request: {e}")
            return None
    @staticmethod
    def options_request(url, headers=None):
        """Make an OPTIONS request to the specified URL and return the allowed HTTP methods."""
        try:
            response = requests.options(url, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.headers.get('Allow', 'No Allow header found')
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while making the OPTIONS request: {e}")
            return None
    @staticmethod
    def connect_request(url, headers=None):
        """Make a CONNECT request to the specified URL and return the response content."""
        try:
            response = requests.request("CONNECT", url, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while making the CONNECT request: {e}")
            return None
        
    @staticmethod
    def trace_http_request(url):
        """Make a TRACE request to the specified URL and return the response content."""
        try:
            response = requests.request("TRACE", url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while making the TRACE request: {e}")
            return None
    @staticmethod
    def is_public_ip(ip_address):
        """Check if the given IP address is a public IP address."""
        try:
            ip = socket.inet_aton(ip_address)
            # Check for private IP ranges, remember to update and add more if a box isn't cooperating. check admin panel for more info if you have one of those boxes.
            private_ranges = [
                (socket.inet_aton("10.0.0.0"), socket.inet_aton("10.255.255.255")),
                (socket.inet_aton("172.16.0.0"), socket.inet_aton("172.31.255.255")),
                (socket.inet_aton("192.168.0.0"), socket.inet_aton("192.168.255.255"))
            ]
            for start, end in private_ranges:
                if start <= ip <= end:
                    return False
            return True
        except socket.error:
            return False
    def extract_cookies(self, response):
        """Extract cookies from an HTTP response."""
        return response.cookies if response else None
    def extract_headers(self, response):
        """Extract headers from an HTTP response."""
        return response.headers if response else None
    def extract_content(self, response):
        """Extract content from an HTTP response."""
        return response.text if response else None
    def extract_status_code(self, response):
        """Extract the status code from an HTTP response."""
        return response.status_code if response else None
    
    def extract_json(self, response):
        """Extract JSON data from an HTTP response."""
        try:
            return response.json() if response else None
        except ValueError:
            print("Response does not contain valid JSON.")
            return None
        
    def extract_links(self, response):
        """Extract links from an HTTP response."""
        if response:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            return [a['href'] for a in soup.find_all('a', href=True)]
        return None
    
