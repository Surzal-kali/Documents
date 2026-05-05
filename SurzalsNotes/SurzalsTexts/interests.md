# Special Interest Groups

	- csp.secureserver.net
	
	- phoenyx.net
	
	- silverseams.com
	
	- centraloffice.com
	
	- electroniccreations.com
	
	- s.exunoplures.org
	
	Notes: These are the domain names of the special interest group. 
	Honeypot checks for past visitors, tabs on old friends. You know, business.

## Characters

### Vuln Machine IPs

#### 1.)  Earth=207 (Apache, Ubuntu 24.04)

    Host: earth.local, terratest.earth.local,
    earth.local/stateOrProvinceName=Sapce

	--- earth is an interesting one, as it only answers to "earth.local", so it specifically is only through mdns.
	Additional commen name is terratest.earth.local, which is interesting, as it is a subdomain of earth.local, but it
	does not resolve to the same IP address. It is likely that this is a red herring, but it is interesting nonetheless.
	The stateOrProvinceName=Space is also interesting, as it is a reference to the fact that the machine is
	in space, and that it is a test machine for space. Ive had this box for an entire college semester and 
	only had brief glimpses into its inner workings.

	--- A brief revelation. It uses a header proxy to resolve the "Earth's Secure Messaging Service" 
	webpage, while reserving the Ipv4 address for the simple Fedora Web Server test page. So its actually making it MORE difficult to communicate with the box, as you have to change the headers in the IDE or 
	proxy with burp to get to the actual webpage.

    ---Alot of my knowledge on earth 
	comes from simple MitM attacks with wireshark, and IDE capture_packets. 
	It obviously is LAN bound only. Unfortunately, while 
	"Earths Secure Messaging Service" is available, its only 
	through proxying with burp or changing the headers 
	manually in the IDE. The fact that it is called "Earths 
	Secure Messaging Service" is interesting, as it is likely 
	a hint that there is something hidden in the messaging 
	service. The fact that it is secure is also interesting. 
	I recall at the beginning of the semester it encrypts the 
	message with the "name" of the sender in the form. 
	However I have not been able to parse the 3 past messages 
	yet, as I don't remember the encryption method used.

    --- In addition, theres an admin login page that has a redirect to get to. 
	No current paths forward there yet, but I think the answer lies in the messages.

	--- After some deliberation, I've come up short on the best path to the next foothold. Mercury, the 
	previous box in the series, was based on SQLi, and a authorative file inclusion. So I think the best 
	path to the next foothold is through the messages, and some sort of cryptographic attack. The fact 
	that the messages are encrypted with the "name" of the sender is interesting, as it is likely that 
	there is something hidden in the encryption method that can be exploited. The fact that it is called 
	"Earths Secure Messaging Service" is also interesting, as it is likely that there are vulnerabilities 
	in the messaging service that can be exploited. I have to figure out how to parse the messages, and 
	then figure out how to exploit any vulnerabilities in the messaging service to get a reverse shell.

	--- Earth was, a journey. Here is the final decoding python script for solving the riddle of the 
	obfuscated messages. It was a xor encryption, base 32 on top, and a drizzle of base36. The key was the username added. 

	The Final messages are a series of numbers. Best guess so far is cursor row ids.  

	Riddle 1: 4162295637467353600
	Riddle 2: 4175322795757723000
	Riddle 3: 4175322795757723000

	Final answer guess:
	Latitude 57°32' N, Longitude 56°14' E (approx 
	from scaling / rounding)
	Which is around Perm region, west of 
	Yekaterinburg, Russia.

	Currently doing a deep pen test with burp using 
	the classic "rock you" word list. It'll take 
	awhile and in the meantime, I'm going to start 
	on Marlinspike, which is the next box in the 
	series.

#### 2.)  Marlinspike=55 (Apache, Ubuntu 16.04)


	--- Marlinspike has a potentially interesting folder, /secret/ a wordpress installation. Secret does not 
	seem to have anything on it's surface, but path traversal is likely. Its brand new to the 
	lineup, and was imported into the lab at the same time as Porteus. 
	It is likely that there is something hidden in the wordpress installation, or that there is a 
	vulnerability in the wordpress installation that can be exploited. The fact that it is 
	called secret is also interesting, as it is likely a hint that there is something hidden in the wordpress 
	installation. The fact that it is a wordpress installation is also interesting, as it is likely that 
	there are vulnerabilities in the wordpress installation that can be exploited. I know for a fact I 
	need to path traversal it. Its on the list. Interestingly enough, the box is a simple wordpress 
	server, and all you have to work with in the guest account is a text editor. So its obvious custom 
	scripting is a must to take full advantage of the box. I have to write my catchingshells.py in the 
	box, execute it, and execute the listening command here. FUN.

	So in order to execute a script, ill have to make a web page that enumerates the targets services for a root service running, and inject a crontab edit to execute the script. I have to be careful with the crontab edit, as it is likely that there is some sort of input validation that can be bypassed with a simple command injection.

#### 3.)  Porteus=157 (Python3 HTTP Web Server)

	 --- Porteus is a dual web server boot to root machine. It 
	has a few interesting webpages, all matrix themed. They
	 sit at 80 and 31337 respectively. 

	The main flag does not in fact sit in root, but the broken guest. 
	Which can't function due to faulty permissions. So the main path to root 
	is through the guest account, which is interesting. Its more of an IT 
	issue than a hacking challenge, but interesting nonetheless. So we have 
	to fix the guest account in order to find the flag maybe? I haven't found it yet.

#### 4.) Mercury=??? (Apache, Ubuntu 18.04)

	--- Mercury is a classic SQLi and file inclusion box. It 
	has a few interesting webpages, but the main one is the 
	"Mercuryfacts" page, which is vulnerable to SQLi. The fact 
	that it is called "Fun facts" is interesting, and im sure i 
	will somehow forget how to get root, but it should be fun 
	to walk the files again. 