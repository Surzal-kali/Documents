#TODO: For the love of god, utilize REST API pfsense routing syntax to script out the network changes needed for different permission enviroments. Fun fact, don't panic, its just curl requests. ez.
#TODO: This will be used to quickly change the network enviroment for different permission levels. 1.) Regular multi-tiered network with a dmz and internal network
#TODO: Test said scripting.

import requests
import json

class Pfsense:
    def __init__(self, host, api_key, api_secret):
        self.host = host
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = f"https://{host}/api/v2/"

    def _headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}:{self.api_secret}"
        }

    def add_firewall_rule(self, rule_data):
        url = f"{self.base_url}/firewall/rules"
        response = requests.post(url, headers=self._headers(), data=json.dumps(rule_data), verify=False)
        return response.json()

    def delete_firewall_rule(self, rule_id):
        url = f"{self.base_url}/firewall/rules/{rule_id}"
        response = requests.delete(url, headers=self._headers(), verify=False)
        return response.json()