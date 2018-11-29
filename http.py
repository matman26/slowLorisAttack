#!/usr/bin/env python

# Imports
from scapy.all import *

# Make a packet
ip = IP(dst="www.google.com")
port = 1235
SYN = ip/TCP(sport=port, dport=80, flags="S", seq=42)
SYN.show()

# Send it and wait for response
SYNACK = sr1(SYN)
SYNACK.show()
# show message we received
