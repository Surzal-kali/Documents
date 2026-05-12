from target_config import SELF_IP_RE, TARGET_INTERFACE, TARGET_IP, TARGET_PASSWORD, TARGET_USERNAME

class Orchestrator:
    def __init__(self):
        self.target_ip = TARGET_IP
        self.target_username = TARGET_USERNAME
        self.target_password = TARGET_PASSWORD

    def orchestrate(self):
        print(f"Orchestrating with target IP: {self.target_ip}, username: {self.target_username}")