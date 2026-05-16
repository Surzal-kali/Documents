import time
import random
import string
import subprocess
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import shutil


#TODO: Make the SleepBaby class more robust, and useful for obfuscation, encoding, and encryption of any data.
# [ ] Random String Generation: Enhance the string_burp method to allow for customizable character sets (e.g., alphanumeric, special characters) and the option to include/exclude certain characters. This can be useful for generating more complex and varied random strings for obfuscation purposes.
# [ ] AES-GCM Encryption/Decryption: Implement AES-GCM encryption and decryption methods that can handle arbitrary input data, allowing for secure encryption of sensitive information. This should include proper handling of encryption keys, initialization vectors (IVs), and authentication tags to ensure data integrity and confidentiality.
# [ ] File Operations with FileShuttle: Integrate the FileShuttle class to manage file operations such as reading, writing, and transferring files securely. This can be useful for handling encrypted data or obfuscated content, allowing for seamless integration of encryption and file management functionalities within the SleepBaby class.
class SleepBaby:
    """A class that provides methods for generating random strings, encrypting and decrypting data using AES-GCM, and managing file operations using the FileShuttle class."""

    def __init__(self, sleep_time=5):
        self.sleep_time = sleep_time

    def string_burp(self, length=10):
        """Generates a random string of the specified length, wrapped in newlines."""
        letters = string.ascii_letters
        raw = ''.join(random.choice(letters) for i in range(length))
        realraw = "\n" + raw + "\n"
        return realraw

    #things to look into to finish this:
    # AES256 Encryption, BASE64 per-case encoding, reverse string before transmission

    def encrypt_with_aes(self, input: str, enc_key: str, iv: str):
        """Encrypts the input string using AES-GCM with the provided encryption key and initialization vector (IV)."""
        key = enc_key.encode()
        nonce = iv.encode() 
        plaintext = input.encode()
        aesgcm = AESGCM(key) 
        ciphertext = aesgcm.encrypt(nonce, plaintext, None)
        ciphertext_str = base64.b64encode(ciphertext).decode()
        return ciphertext_str
        
    def decrypt_with_aes(self, input: str, enc_key: str, iv: str):
        """Decrypts the input string using AES-GCM with the provided encryption key and initialization vector (IV)."""
        key = enc_key.encode()
        nonce = iv.encode()
        ciphertext = base64.b64decode(input)
        aesgcm = AESGCM(key)     
        decrypted = aesgcm.decrypt(nonce, ciphertext, None)
        return decrypted.decode()
       
    def generate_iv_string(self, length=6):
        """Generates a random string of the specified length to be used as an initialization vector (IV) for encryption."""
        chars = string.ascii_letters + string.digits + "#$()*+,-.:;<=>?@[]_"
        return ''.join(random.choices(chars, k=length))
