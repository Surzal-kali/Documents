import time
import random
import string
import subprocess
import os
import shutil

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

#runtime discrepencies per cryptographic protocols
#runtime discrepencies per file size

