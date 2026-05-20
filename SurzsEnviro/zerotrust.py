import json
import cryptography.hazmat.primitives.asymmetric.rsa as rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes   
import os
import time


class ZeroTrust:
    """A class to implement zero trust security principles using RSA encryption for secure communication between components."""
    def __init__(self, private_key_path, public_key_path):
        """Initialize the ZeroTrust class with paths to the private and public keys."""
        self.private_key_path = private_key_path
        self.public_key_path = public_key_path
        self.private_key = None
        self.public_key = None
        self.load_keys()

    def load_keys(self):
        """Load the private and public keys from the specified paths, or generate new keys if they do not exist."""
        if os.path.exists(self.private_key_path) and os.path.exists(self.public_key_path):
            with open(self.private_key_path, "rb") as key_file:
                self.private_key = serialization.load_pem_private_key(
                    key_file.read(),
                    password=None,
                )
            with open(self.public_key_path, "rb") as key_file:
                self.public_key = serialization.load_pem_public_key(
                    key_file.read()
                )
        else:
            self.generate_keys()

    def generate_keys(self):
        """Generate a new RSA key pair and save them to the specified paths."""
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        self.public_key = self.private_key.public_key()
        with open(self.private_key_path, "wb") as key_file:
            key_file.write(
                self.private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption(),
                )
            )
        with open(self.public_key_path, "wb") as key_file:
            key_file.write(
                self.public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo,
                )
            )

    def encrypt_message(self, message):
        """Encrypt a message using the public key."""
        ciphertext = self.public_key.encrypt(
            message.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        return ciphertext

    def decrypt_message(self, ciphertext):
        """Decrypt a message using the private key."""
        plaintext = self.private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        return plaintext.decode()