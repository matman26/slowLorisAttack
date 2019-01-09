#!/usr/bin/env python

# Imports
from scapy.all import *
from request_http import *
import time
import random

def main():
    ip_address = "35.204.165.14"
    port = 4213 #random.randint(1024,6000)
    list_size = 200
    my_list = list(range(port, port + list_size))

    print(my_list)
    for port_number in my_list:
        httpRequest(ip_address,port_number)
    
    # Make requests
    '''
    while True:
        for i in range(0,100):
            send_get("192.168.1.50")
        time.sleep(10)
    '''

if __name__== "__main__":
    main()

