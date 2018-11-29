#!/usr/bin/env python

# Imports
from scapy.all import *
import time

# Make a TCP SYN
ip = IP(dst="35.204.58.85")
get='GET / HTTP/1.0\n\n'
port = RandNum(1024,6500)
SYN = ip/TCP(sport=port, dport=80, flags="S", seq=42)

# Send SYN and wait for SYNACK
SYNACK = sr1(SYN)
SYNACK.show()

# Send ACK and GET
ACKGET=ip/TCP(sport=SYNACK.dport, dport=80, flags="A", seq=SYNACK.ack, ack=SYNACK.seq + 1)/get
reply,error=sr(ACKGET)
reply.show()
