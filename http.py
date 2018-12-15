#!/usr/bin/env python
# Imports
from scapy.all import *
#import time
#import subprocess

# Make a TCP SYN
#ip_address="35.204.58.85" # Alessandro's server
#my_port=80                # Alessandro's server

ip_address="192.168.33.10"    # My VM (vagrantfile)
my_port=80                    # My VM

ip = IP(dst=ip_address)
get = 'GET / HTTP/1.1\r\nHost: 192.168.33.10\r\n\r\n'

#get_arguments = ip_address + ":" + my_port
#print(get_arguments)
#print("GET " + get_arguments)
#subprocess.check_output(["lwp-request","-m get",get_arguments],shell=True)

port = RandNum(1024,6500)
SYN = ip/TCP(sport=port, dport=my_port, flags="S", seq=42) # 80 if remote server, 8080 on VM (see Vagrantfile)

# Send SYN and wait for SYNACK
print(SYN.summary())
SYNACK = sr1(SYN)

# Send ACK and GET
ACK=ip/TCP(sport=SYNACK.dport, dport=my_port, flags="A", seq=SYNACK.ack, ack=(SYNACK.seq+1))/get
#send(ACK)

#GET=ip/TCP(sport=ACK.sport, dport=ACK.dport, seq=ACK.ack+1, ack=(ACK.seq+2))/get
data=sr1(ACK)
data.show()

