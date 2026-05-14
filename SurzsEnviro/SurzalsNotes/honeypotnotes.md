# Honeypot Notes

## What is a Honeypot?

A honeypot is a security mechanism set up to detect, deflect, or study attempts to gain unauthorized access to information systems. It is designed to appear as a legitimate target to attackers, while actually being a decoy that allows security professionals to monitor and analyze attack techniques. The main question i have for this doc is: can you utilize a honeypot for more than just being a trap on the other side of the network? Can you use it to actually gather information on the defender's methods and techniques? it IS just more containerized, right? so it should be able to be used for more than just a trap, it should be able to be used for gathering information on the defender's methods and techniques as well.

## Types of Honeypots

1. **Low-Interaction Honeypots**: These honeypots simulate only a limited set of services and interactions. They are easier to set up and maintain but may not provide as much information about the attacker's methods. Common simulated services include web servers, FTP servers, and SSH servers.

2. **High-Interaction Honeypots**: These honeypots simulate a full operating system and allow attackers to interact with it as they would with a real system. They provide more detailed information about the attacker's techniques but require more resources and maintenance. These usually simulate a full graphical interface and allow attackers to perform a wide range of attacks.

Production: Deployed in corporate networks to lure attackers away from actual production servers and source code.

Research: Used by security researchers to study attack techniques and gather intelligence on emerging threats.

Benefits: Reduces false positives in security monitoring, provides high-fidelity, actionable data on new threats, and helps identify weak points in existing infrastructure.

Risks: If poorly configured or insufficiently isolated, a honeypot can be used by hackers as a pivot point to enter the actual production network. there it is... yes it can be a pivot point if not properly configured and isolated, which is why it's important to ensure that the honeypot is properly configured and isolated to prevent it from being used as a pivot point by attackers, but can it be a chained interaction as part of a honeynet? a deliberate red herring to keep user interaction and attention on the honeypot while the actual data and most likely cause for their intrusion is safely out of reach. An infinite doorway to keep them busy while you gather information on their methods and techniques, and then use that information to improve your defenses and protect your actual production network.

# Deployment Strategies

pick up again at https://dev.to/trixsec/how-to-set-up-a-honeypot-for-cyber-attacks-4c08 later