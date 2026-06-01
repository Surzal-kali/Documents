from catchingpackets import PacketSniffer
from httpme import HttpMe
from computerspeak import ComputerSpeak
import time
from packetcraft import PacketCraft

class FreshMeat:
    def __init__(self):
        self.sniffer = PacketSniffer()
        self.httpme = HttpMe()
        self.speaker = ComputerSpeak()
        self.crafter = PacketCraft()
    def wait_for_new_devices(self, timeout=30):
        self.speaker.speak("Starting to sniff for new devices...")
        new_device = self.sniffer.wait_for_new_device(timeout=timeout)
        if new_device:
            self.speaker.speak(f"New device detected: {new_device}")
            return new_device
        else:
            self.speaker.speak("No new devices detected within the timeout period.")
            return None
    def run(self):
        self.speaker.speak("FreshMeat is now running. Waiting for new devices to connect...")
        while True:
            new_device = self.wait_for_new_devices(timeout=30)
            if new_device:
                self.speaker.speak(f"New device detected: {new_device}. Attempting to interact...")
                # Here you could add code to interact with the new device, e.g., send a welcome message, perform a scan, etc.
                # For demonstration, we'll just wait a bit and then continue listening for new devices.
                time.sleep(5)
            else:
                self.speaker.speak("No new devices detected in the last 30 seconds. Still waiting...")