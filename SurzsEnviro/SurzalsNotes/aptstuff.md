# Play #1: The Island Hopper (Supply Chain Entry)

The Concept: Why attack the fortress gate when you can poison the bread delivered to the kitchen?
The Sequence:
The target is a defense contractor with superb perimeter security. The attacker identifies a small HVAC vendor that has persistent VPN credentials into the target’s billing system. The vendor’s website runs a vulnerable PHP plugin.

Recon: Passive DNS and job postings reveal the vendor relationship.

Initial Access: Exploit the plugin, drop a web shell on the vendor’s public-facing server.

Pivot: From the vendor’s server, locate the VPN configuration file and stored credentials.

Bridgehead: Dial into the target’s network using the legitimate vendor VPN, blending into normal administrative traffic.

Lateral Movement: Once inside, pass-the-hash to a development server, then to the air-gapped engineering network via a misconfigured jump host that occasionally has USB file transfer access.

The beauty is the noise-to-signal ratio. The initial breach looks like script-kiddie activity against a low-value target. By the time the attacker appears inside the military contractor’s core network, they’re using legitimate credentials and encrypted VPN tunnels. Every log entry looks like "HVAC_Vendor_Admin."

# Play #2: The Living-Off-The-Land Jamboree

The Concept: Don’t bring a gun to a knife fight if the kitchen is full of knives. Use tools already trusted by the operating system.

## TLDR:

1. Use built-in tools (PowerShell, WMI, PSExec) to avoid dropping new binaries.
2. Schedule tasks or use services to maintain persistence without new executables.
3. Exploit trust relationships (e.g., signed scripts, trusted certificates) to blend in with normal activity.
4. Use encrypted channels (e.g., HTTPS, DNS tunneling) to exfiltrate data without raising suspicion.

So in essence, APT and RAT simulations and techniques revolve around living off the land, blending in with normal activity, and exploiting trust relationships. The attacker’s goal is to be invisible while they move through the network, exfiltrate data, or achieve their objectives.

 # Don't be seen, don't be heard, and above all, wait. Time is your friend.

:D will be back with more notes on APT techniques and strategies. Stay tuned!

# Musings

     It occurs to me, that trying to set up at-home apt simulations is harder than originally conceived. 
     You have to not only update the ai model, but i personally think should enumerate often. just lots of logic problems nested into one idea.
     Yet it sounds so very worth it. I want to practice and understand APT and RAT techniques for myself, and without a lab partner to play blue team, i am forced to turn to automation.
     will i lose some? definitely. will my code and technique improve tho? 1000%
     
the more i think about the logic and behavior needed for long-term persidtence, the more i smell a challenge :D. and a better way to carry myself in cyberspace

## If u do everything right, people wont be sure u did anything at all

so the apt simulation has 3 sides

kali: meeeee

pfsense: router and network chatter box (use crontab and bash scripting)

ubuntu server?: a vm specifically for regex and pattern matchint telemtry from the network/hosts

im not sure on the specifics on the ubuntu server, but the pfsense is pure bash

oh and probably a malware production server(s)
