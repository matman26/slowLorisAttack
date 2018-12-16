#!/usr/bin/env python
# Imports
from scapy.all import *
from scapy.all import http

# This handles HTTP responses from the server
def handle(pkt):
    if pkt.haslayer(http.HTTPrequest):
        print(pkt)
    
# Make a TCP SYN
#ip_address="35.204.58.85"    # Alessandro's server
ip_address="192.168.33.10"    # Matheus' VM (see Vagrantfile)
server_port=80                # http port
ip = IP(dst=ip_address)       # IP Packet 

# HTTP GET Request
get = "GET / HTTP/1.1\r\nHost: " + ip_address + "\r\n\r\n"
port = RandNum(1024,6500)

# The TCP 3-way handshake rules must be followed. As such, we begin by sending a
# TCP packet with the S (or SYN) flag set. The sequence number is irrelevant, as all
# future TCP packets will contain sequence numbers which are increments of the number
# given
SYN = ip/TCP(sport=port, dport=server_port, flags="S", seq=42) 

# Send SYN and wait for SYNACK as response
print(SYN.summary())
SYNACK = sr1(SYN)

# Send ACK and finally HTTP GET, sniff for the result
ACK=ip/TCP(sport=SYNACK.dport, dport=server_port, flags="A", seq=SYNACK.ack, ack=(SYNACK.seq+1))/get
sniff(filter="tcp and port 80", store=False, prn=handle)
