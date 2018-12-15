#!/usr/bin/env python
# Imports
from scapy.all import *

# Make a TCP SYN
#ip_address="35.204.58.85"    # Alessandro's server
ip_address="192.168.33.10"    # Matheus' VM (see Vagrantfile)
my_port=80                    # www port

ip = IP(dst=ip_address)
# HTTP GET Request
get = 'GET / HTTP/1.1\r\nHost: 192.168.33.10\r\n\r\n'
port = RandNum(1024,6500)
SYN = ip/TCP(sport=port, dport=my_port, flags="S", seq=42) 

# Send SYN and wait for SYNACK
print(SYN.summary())
SYNACK = sr1(SYN)

# Send ACK and GET
ACK=ip/TCP(sport=SYNACK.dport, dport=my_port, flags="A", seq=SYNACK.ack, ack=(SYNACK.seq+1))/get
data=sr1(ACK)
data.show()

