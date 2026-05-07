import time
import random
import string
import subprocess
import os
from fileshuttle import FileShuttle as fs
#hello from my phone
class SleepBaby:
    def __init__(self, sleep_time=5):
        self.sleep_time = sleep_time
        self.fs = fs()

    def random_string(self, length=10):
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for i in range(length))

#things to look into to finish this:

#runtime discrepencies per cryptographic protocols
#runtime discrepencies per file size

