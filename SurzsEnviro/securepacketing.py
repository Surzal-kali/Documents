from  sleepbaby import SleepBaby
from  zerotrust import ZeroTrust
from  packetcraft import PacketCraft
from target_config import TARGET_IP, SELF_IP_RE
import random


TARGET_PORT = 12345

class SecurePacketing:
    """A class that combines the functionalities of SleepBaby, ZeroTrust, and PacketCraft to provide secure packet crafting and transmission capabilities."""

    def __init__(self):
        self.sleepbaby = SleepBaby()
        self.zerotrust = ZeroTrust(private_key_path="private_key.pem", public_key_path="public_key.pem")
        self.packetcraft = PacketCraft()
    # i guess i gotta generate that off script and load it in here, or maybe i can just generate it on the fly every time, since it's only used for one message at a time. yeah let's do that, it's simpler and more secure to generate a fresh key for each message.
    def create_secure_packet(self, data: str, enc_key: str, iv: str):
        """Creates a secure packet by encrypting the input data and crafting it into a packet format."""
        encrypted_data = self.sleepbaby.encrypt_with_aes(data, enc_key, iv)
        secure_data = self.zerotrust.encrypt_message(encrypted_data)
        packet = self.packetcraft.craft_udp_packet(payload=secure_data, src_ip=SELF_IP_RE, dst_ip=TARGET_IP, dst_port=TARGET_PORT, src_port=random.randint(1024, 65535))
        return packet
    
    def send_secure_packet(self, packet):
        """Sends the crafted secure packet to the target destination."""
        self.packetcraft.send_packet(packet)

    def decrypt_secure_packet(self, packet, enc_key: str, iv: str):
        """Decrypts a received secure packet to retrieve the original data."""
        secure_data = self.packetcraft.extract_payload(packet)
        encrypted_data = self.zerotrust.decrypt_message(secure_data)
        decrypted_data = self.sleepbaby.decrypt_with_aes(encrypted_data, enc_key, iv)
        return decrypted_data


# （づ￣3￣）づ╭❤️～ APPROVED CONCEPT 