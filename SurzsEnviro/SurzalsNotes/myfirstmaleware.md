# APT Enviro Notes

first things first, we need to be able to

       we need to find a way to make a tmp container or user. something out of sight out of mind to operate within. maybe we can use the sleep class to create a random user and then delete it after were done, or even better, have it create a random user and then have it sleep for a certain amount of time before deleting it, so that it looks like a normal user account that was created and then deleted after a certain amount of time.

the more i think about it, the more a venv or container sounds best

1. know our enviroment and adjacent local neighbors

       we need to first enumerate the specs and command prefix/bin/path of the host. but slowly? maybe a dynamic sleep class that can partition the functions passed through it. 

       We could always save the script, and have this class be a psuedo scheduler that can run the script at certain times, or even better, have it run at random intervals, breaking the scripts by line and running each line at a random interval, with a max and min sleep time.

2. Identify any vulnerabilities in the enviroment and adjacent local users. This might be data analysis broken by the above mentioned sleep class.

3. if were going to disguise our traffic, we first have to know the day-2-day. wiretap away

this should probably be a cron job for a random amount of time, and then we can use the data to create a profile of the network traffic, and then we can use that profile to create a camouflage for our exfiltration.

       if im supposed to be emulating an APT, then the next step would be to encrypt and compress the data inside of a hidden directory and sleep for a certain amount of time, preferably during busiest network times, or even better when its a skeleton crew on watch

## Answers to above, and follow ups

making a temp user or container is too loud and system heavy. think more venv and generated bins that can easily rm.

know local user and enviro: i feel like this is alot of tapping localhost
in addition, walking bin/path to get the lay of the land.

2 and 3 are partially case by case basis, but ill circle back to this section to update when im further along.

IN ADDITION. the exfiltration and obfuscation of data is going to be a huge component of this for me. mostly cause im sick of my own firewall deleting my code repo cause its malware. so im going to have to get creative with how i store and exfiltrate my data, and how i obfuscate my code to avoid detection. Compression however, needs to not be used. Unless the host is so tiny we must, then best not add even MORE strain to our victim system than our presence already does.