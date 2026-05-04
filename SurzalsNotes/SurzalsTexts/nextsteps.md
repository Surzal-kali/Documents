# (❁´◡`❁) Next Steps

## The Machines

### 1.)  Earth=207 (Apache, Ubuntu 16.04)

        It needs some deal with crypotgraphy (my only weakness) and the secure messaging service. I need to decipher the three past messages listed in the site, to gain access to the admin panel for the website and bust permissions.

        #### The Messages:
        The messages are encrypted with the "name" of the sender, which is interesting, as well as reversing the string before encrypting it. I don't know the actual encryption method, so fuck this level. Yet its the oldest one of the lot, it deserves retirment. I'm sick of seeing that shitty stock image on my network.

        The Message encryption is XOR with base 32 on top. Below are the deobfuscated messages
        VMFMNUKBDZMI…YWE
        VPZWEKGQ7QYK…PV
        VPZWEKGQ7QYK…KJ7

### 2.)  Marlinspike=55 (Apache, Ubuntu 16.04)

        My favorite one right now OHMYGOD. Its a fishtank. Its amazing. Its got a guest account that operates in the system memory. And its HELLA OUTDATED BABY. So we're going to work on this one concurrently with earth, as it will serve as a pivot point for the next machines. It even resets the box on power off. so lets never turn this thing off unless we absolutely fucked up. Yeth.

        #### The Guest Bin:

        It seriously has so many different ways it can be hacked, because the container is leaked, so it spills into the system files (barely, its a misconfiguration and a bug after all). 
        So we can read the guest profile default bin, the way it's cron jobs are, and how it backups its files despite being ephemeral. The virtual "virtual" network is known as Windows Network, so both the container and the vm are concurrently running, and the End Goal is on a seperate virtualx2 network. This inception bullshit makes my head hurt.

        ### Update Logs:

        After checking the system files why yes captain I can read the entire site likes its a maze on a cracker jack box. ITS G-R-E-A-T.  However up on even FURTHER testing, i've concluded that the earlier spotted mysql database in bash/bin is running elsewhere on the system or not at all, not associated with the wordpress installation so we have no access to it yet. Nor can we execute scripts from the machine that are custom, however we CAN connect to a web server that we control, so we can serve a web payload and execute it on the machine, which is really cool. So we can use the guest account to connect to a web server that we control, and serve a web payload that will give us a reverse shell on the machine. This is exactly the banana-panzaz shit I wanted to do. I'm all in.

### 3.) Porteus=157 (Python3 HTTP Web Server)

        --- Porteus is a dual web server boot to root machine. It has a python3 http web server, and a countdown timer that is vulnerable to cross-site scripting. So we will be working on this one concurrently with the other two machines, as it will serve as a pivot point for the next machines. The countdown timer is likely the main attack vector for this machine, as it is likely that there is something hidden in the countdown timer that can be exploited. Ironic that of course when the timer breaks, its a "zero-day" countdown AND vulnerability. 
        
        #### The Countdown Timer
        So the main breakage with the scripting of this website, and why its vulnerable. IS IN FACT THE COUNTDOWN TIMER. It calls for "someVariable" so that the countup from 2018/10/17 to the current date can be calculated. But the variable is never defined, so we can put whatever we want in there. Cross site scripting ahoy! I love writing malware and coding so much. This gift is truly a blessing. 
        
        However to make this extra efficient, i've decided to tackle this machine last after MarlinSpike specifically is popped. Then we can do a chain attack and use the reverse shell from Marlin to execute the payload on Porteus, which would be really cool. :D Two boxes at once, and a chain attack. I'm so excited.
