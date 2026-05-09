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
        ciphertext=aesgcm.encrypt(nonce, plaintext, None)
        ciphertext_str = base64.b64encode(ciphertext).decode()
        return ciphertext_str
        
   def decrypt_with_aes(input:str, enc_key: str, iv: str)
       key = enc_key.encode()
       nonce = iv.encode()
       ciphertext = base64.b64decode(input
       aesgcm = AESGCM(key)     
       decrypted = aesgcm.decrypt(nonce, ciphertext, None)
       return decrypted.decode()
       
  def generate_iv_string(length=6
      chars = string.ascii_letters + string.digits + "#$()*+,-.:;<=>?@[]_"
      return ''.join(random.choices(chars, k=length))     
      
 enc_key = "1Xt5YfM4ZNuFdwp3OfVkwkhhQLagWKtt"
 iv = generate_iv_string(12)
 input = "F OFF"
 
 ciphertext = encrypt_with_aes(input, enc_key, iv)
 print("Ciphertext:", ciphertext) 
 
 decrypted = decrypt_with_aes(ciphertext, enc_key, iv)
 print("Decrypted:", decrypted
   