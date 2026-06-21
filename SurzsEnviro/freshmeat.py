from catchingpackets import PacketSniffer
from httpme import HttpMe
from computerspeak import ComputerSpeak
import time
from packetcraft import PacketCraft
from netrunning import NetRunning
#ok ai assistant's take on the FRESHMEAT class is (honeypot was a better idea than i had)

#so originally,, for my capstone I had the idea to build this out as the beginning "detector" for the presentation's automated exploit chain at work. The idea was to have it run in the background, and when a new device connected to the network, it would detect it, speak out loud about it, and then attempt to interact with it (send ARP requests, do some basic HTTP probing, etc). Critically, we'd hardcode the presentation logic to the MAC and IP of our "victim" machine, so no one accidentally gets anything. 
class FreshMeat:
    def __init__(self):
        self.sniffer = PacketSniffer()
        self.httpme = HttpMe()
        self.speaker = ComputerSpeak()
        self.crafter = PacketCraft()
        self.network = NetRunning()
    def wait_for_new_devices(self, timeout=30):
        """Return structured device info or None.
        Returns dict {'ip': str|None, 'mac': str|None, 'proto': str} when a device is seen.
        """
        self.speaker.speak("Starting to sniff for new devices...")
        new_device = self.sniffer.wait_for_new_device(timeout=timeout)
        if new_device:
            ip = new_device.get("ip")
            mac = new_device.get("mac")
            if ip:
                if mac:
                    self.speaker.speak(f"New device detected: {ip} ({mac})")
                else:
                    self.speaker.speak(f"New device detected: {ip}")
            else:
                if mac:
                    self.speaker.speak(f"New device detected: MAC {mac} (IP unknown)")
                else:
                    self.speaker.speak("New device detected: unknown device")
            return new_device
        else:
            self.speaker.speak("No new devices detected within the timeout period.")
            return None
    def run(self):
        self.speaker.speak("FreshMeat is now running. Waiting for new devices to connect...")
        while True:
            new_device = self.wait_for_new_devices(timeout=30)
            if new_device:
                ip = new_device.get("ip")
                mac = new_device.get("mac")
                if ip:
                    self.speaker.speak(f"New device detected: {ip} ({mac}). Attempting to interact...")
                    packet = self.crafter.craft_arp_request(
                        src_mac="00:11:22:33:44:55",
                        src_ip="192.168.1.100",
                        target_ip=ip,
                    )
                    self.crafter.send_packet(packet)
                    self.sniffer.start_sniffing(filter=f"arp and host {ip}")
                    self.speaker.speak(f"Sent ARP request to {ip}. Sniffing for responses...")
                    response = self.crafter.wait_for_packet(filter=f"arp and host {ip}", timeout=10)
                    if response:
                        self.speaker.speak(f"Received ARP response from {ip}. Device is active and responsive.")
                        self.network.scan_network(ip, nmap_args="-sV")
                        for port in [80, 443]:
                            url = f"http://{ip}:{port}"
                            self.speaker.speak(f"Attempting HTTP request to {url}...")
                            http_result = self.httpme.http_request("GET", url, timeout=3)
                            if http_result['ok']:
                                self.speaker.speak(f"Received response from {url}: {http_result['status_code']} {http_result['reason']}")
                            else:
                                self.speaker.speak(f"No response from {url}. It may be closed or filtered.")

                else:
                    # Safe behavior: do not attempt ARP targeting without a known IP.
                    self.speaker.speak(f"Device {mac} has no IP yet; skipping ARP probe and logging for follow-up.")
                    try:
                        with open('missing_ip_devices.log', 'a', encoding='utf-8') as fh:
                            fh.write(f"{mac}\n")
                    except Exception:
                        pass
            else:
                self.speaker.speak("No new devices detected in the last 30 seconds. Still waiting...")
                self.speaker.speak("K bye")
                break
    def ctf_run(self): #this is the part i gotta fixeth. 
        """Run in VPN/CTF environment where new devices may appear frequently, and broadcast ARP probing yields no results."""
        pass 
