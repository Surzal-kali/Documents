import time
import random
import string
import subprocess
import os
from fileshuttle import FileShuttle as fs
#hello from my phone
class SleepBaby():
    def __init__(self, sleep_time=5):
        self.sleep_time = sleep_time
        self.fs = fs()

    def random_string(self, length=10):
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for i in range(length))

    def hiccup(self):
        print(f"Sleeping for {self.sleep_time} seconds...")
        time.sleep(self.sleep_time)
        random_str = self.random_string()
        return f"Woke up! Here's a random string: \n{random_str}\n"

        #so we need this to be able to append a file with the sectioned payloads, at random intervals of low system activity. this will be the evasion and LotL module for crafting a hidden dev enviroment. Data exfiltrarion will probably have to be a custom per enviroment module, so this will focus on obfuscated storage

