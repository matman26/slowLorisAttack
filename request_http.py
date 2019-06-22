#!/usr/bin/env python
# Imports
from scapy.all import *
import random
import time

# TITLE: request_http.py
# AUTHORS: Matheus Augusto da Silva; Alessandro Montaldo
# OBS: The following command stops Linux machines from dropping
# the TCP connection started by scapy (run as root):
# iptables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP

# This function sends a GET Request in HTTP 1.1 after the TCP 3-way handshake and
# returns information on the state of the TCP connection

# This returns the length of the packet we just sent (to update the sequence numbers later)
def utf8len(s):
	return len(s)

# This makes a TCP Three-way Handshake and returns the last packet sent(Incomplete GET Request)
def httpRequest(ip_address,source_port,sequence_number=42): 
    server_port=80                # http port
    ip = IP(dst=ip_address)       # IP Packet 

    # GET Request missing the last line break character
    get = ("GET /14 HTTP/1.1\r\n")

    # The TCP 3-way handshake rules must be followed. As such,
    # we begin by sending a TCP packet with the S (or SYN) flag set.
    SYN = ip/TCP(sport=source_port, dport=server_port, flags="S", seq=42) 

    # Send SYN and wait for SYNACK as response
    SYNACK = sr1(SYN,verbose=False,retry=3,timeout=2)
    myack=SYNACK.seq + 1

    # Send ACK and finally HTTP GET
    ACK = ip/TCP(sport=source_port, dport=server_port, flags="A", seq=SYNACK.ack, ack=myack)
    send(ACK,verbose=False)
    GET = ip/TCP(sport=source_port, dport=server_port, seq=SYNACK.ack, flags = "PA" , ack=myack)/get
    send(GET,verbose=False) 
    
    # Return GET to set up the correct Sequence and Acknowledgement Number for each socket on main
    return GET
