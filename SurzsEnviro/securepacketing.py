from SurzsEnviro.sleepbaby import SleepBaby
from SurzsEnviro.zerotrust import ZeroTrust
from SurzsEnviro.packetcraft import PacketCraft
from target_config import TARGET_IP, SELF_IP_RE, TARGET_INTERFACE
import random

# TODO: Fix SecurePacketing to match the current ZeroTrust and PacketCraft APIs.

TARGET_PORT = 12345

class SecurePacketing:
    """A class that combines the functionalities of SleepBaby, ZeroTrust, and PacketCraft to provide secure packet crafting and transmission capabilities."""

    def __init__(self):
        self.sleepbaby = SleepBaby()
        self.zerotrust = ZeroTrust()
        self.packetcraft = PacketCraft()
    
    def create_secure_packet(self, data: str, enc_key: str, iv: str):
        """Creates a secure packet by encrypting the input data and crafting it into a packet format."""
        encrypted_data = self.sleepbaby.encrypt_with_aes(data, enc_key, iv)
        secure_data = self.zerotrust.encrypt_message(encrypted_data)
        packet = self.packetcraft.craft_udp_packet(payload=secure_data, dst_ip=TARGET_IP, dst_port=TARGET_PORT, src_port=random.randint(1024, 65535))
        return packet
    
    def send_secure_packet(self, packet):
        """Sends the crafted secure packet to the target destination."""
        self.packetcraft.send_packet(packet, TARGET_INTERFACE)

    def decrypt_secure_packet(self, packet, enc_key: str, iv: str):
        """Decrypts a received secure packet to retrieve the original data."""
        secure_data = self.packetcraft.extract_payload(packet)
        encrypted_data = self.zerotrust.decrypt_message(secure_data)
        decrypted_data = self.sleepbaby.decrypt_with_aes(encrypted_data, enc_key, iv)
        return decrypted_data

# Checklist:
# [ ] Initialize ZeroTrust with required private_key_path and public_key_path arguments.
# [ ] Pass a real src_ip into PacketCraft.craft_udp_packet(...); the current call is missing it.
# [ ] Stop passing TARGET_INTERFACE into send_packet(...); PacketCraft already stores the interface on self.interface.
# [ ] Remove unused imports if they are not needed after the wiring is fixed.
# [ ] Recheck whether SELF_IP_RE should be replaced with an actual source IP configuration value.



#  - generate a fresh random AES key per session or message
#  - generate a fresh unique nonce per message
#  - encrypt payload once with AES-GCM
#  - use RSA only to exchange/protect the AES key, or use signatures for authenticity
#  - send metadata + ciphertext in the packet payload