# SEPERATE DEPENDENCIES NEEDED FOR THE PROJECT

Metasploit Framework:

Clang

Hurl

tshark

scapy


alot of time on your hands to systemically enumerate and discover the vulnerabilities in the project and then write exploits for them....by hand. ai can lint (and probably draft/bounce ideas off of like i do) but can it machine speak? i thought not.

you need to know the system you're querying, and be absolutely positive you know what your doing with the system api of the system you're installing this on. Both matter way more than normal.

(The crypticness is on purpose i assure)

this project is a translator when put it simply. treat it like such and exploit its adaptability, and specifity.

also also also

this will EVENTUALLY have a installer script but for now

git clone

cd Documents

python3 -m venv venv

source venv/bin/activate 

pip install -r requirements.md

(tada u have basic py functionality)

but also........

primarily this tiny thing will be a Remote Execution Endpoint. So we need our good pal metasploit, headless, with bare min overhead so

msfrpcd -P <PASSWORD> -S -a 127.0.0.1 

or however thats spelt if youre not on kali-rolling proper. 

we just need the basic api to query our payloads and such :D


# Fancy Tips Ill Automate Later

if you want to keep the ipython3 repl init super short and clean

touch export.txt

nano export.txt

export MSF_PASS=<PASSWORD>
export TARGET_INTERFACE=<Net-Interface-Here> (this ones different linux v windows and i cant fucking recall windows cause fuck windows)
export TARGET_IP=<xxx.xxx.xxxx.xxx>
export TARGET_PASSWORD=" "
export TARGET_USERNAME=<insert username or empty quotes>
export SELF_IP_RE=<xxx.xxx.xxx.xxx/xx>
export TARGET_RANGE=<xxx.xxx.xxx.xxx/xx>


then everytime you wanna launch its just

cat export.txt

(copy and paste the output back into shell)

ipython3

BAM YOU'RE DONE THE JOURNEY IS OVER.
