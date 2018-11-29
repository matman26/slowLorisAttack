#!/usr/bin/env python

# Imports
from scapy.all import *

def send_get(ip_addr):
    ip = IP(dst=ip_addr)
    get='GET / HTTP/1.0\n\n'
    port = RandNum(1024,6500)
    SYN = ip/TCP(sport=port, dport=80, flags="S", seq=42)

    # Send SYN and wait for SYNACK
    SYNACK = sr1(SYN)

    # Send ACK and GET
    ACKGET=ip/TCP(sport=SYNACK.dport, dport=80, flags="A", seq=SYNACK.ack, ack=SYNACK.seq + 1)/get

    send(ACKGET)

def main():

    # Make requests
    send_get("35.204.58.85")




if __name__== "__main__":
    main()
