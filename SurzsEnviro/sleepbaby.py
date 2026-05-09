import time
import random
import string
import subprocess
import base64
from cryptography.haxmat.primitves.ciphers.aead import 
import os
import shutil
from fileshuttle import FileShuttle as fs

#hello from my phone
class SleepBaby:
    def __init__(self, sleep_time=5):
        self.sleep_time = sleep_time
        self.fs = fs()

    def string_burp(self, length=10):
        letters = string.ascii_letters
        raw = ''.join(random.choice(letters) for i in range(length))
        realraw = "\n" + raw + "\n"
        return 

#things to look into to finish this:

# AES256 Encryption, BASE64 per-case encoding, reverse string before transmission

    def encrypt_with_aes(input:str, enc_key: str, iv: str):
        key = enc_key.encode()
        nonce = iv.encode() 
        plaintext = input.encode()
        aesgcm = AESGCM(key)
        
        ciphertext_str = base64.b64encode(ciphertext).decode()
        return ciphertext_str