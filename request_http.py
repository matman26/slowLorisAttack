#!/usr/bin/env python
# Imports
from scapy.all import *
# from scapy.layers import http
import scapy_http.http
import random

# TITLE: http.py
# AUTHORS: Matheus Augusto da Silva; Alessandro Montaldo
# OBS: The following command stops Linux machines from dropping
# the TCP connection started by scapy (run as root):
# iptables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP

# This function sends a GET Request in HTTP 1.1 and sniffs for the 200 OK packet
# after the 3-way handshake
# For the next part of the project, this will be restructured into a function
# which receives and IP address & port number and returns the HTTP response to the GET

# This handles HTTP responses from the server
#def handle(pkt):
    #if pkt.haslayer(scapy_http.http.HTTPRequest):
        #pkt.show()

# Make a TCP SYN
def httpRequest(ip_address,source_port):
    #ip_address="35.204.58.85"    # Alessandro's server
    #ip_address="192.168.33.10"    # Matheus' VM (see Vagrantfile)
    #ip_address="35.204.165.14"
    #source_port = random.randrange(1024,6500)

    server_port=80                # http port
    ip = IP(dst=ip_address)       # IP Packet 
    # HTTP GET Request
    get = ("GET / HTTP/1.1\r\nHost: "
        + ip_address
        + "\r\nConnection: keep-alive\r\n")

    # The TCP 3-way handshake rules must be followed. As such,
    # we begin by sending a TCP packet with the S (or SYN) flag set.
    SYN = ip/TCP(sport=source_port, dport=server_port, flags="S", seq=42) 

    # Send SYN and wait for SYNACK as response
    SYN.show()
    SYNACK = sr1(SYN)

    # Send ACK and finally HTTP GET, sniff for the resultACK = ip/TCP(sport=SYNACK.dport, dport=server_port, flags="A", seq=SYNACK.ack, ack=(SYNACK.seq+1))
    ACK = ip/TCP(sport=SYNACK.dport, dport=server_port, flags="A", seq=SYNACK.ack, ack=(SYNACK.seq+1))
    GET = ip/TCP(sport=ACK.sport, dport=server_port, seq=ACK.seq, flags = 24 , ack=(ACK.ack))/get
    send(ACK)
    REPONE =sr(GET) 
    SECACK = ip/TCP(sport=source_port , dport=server_port, flags="A", seq=REPONE.ack, ack=(REPONE.seq+1))
    #sniff(filter="tcp and port 80", store=False, prn=handle) # we'll improve on this later 
