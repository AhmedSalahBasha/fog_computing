#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 23:56:22 2019

@author: basha
"""


import socket    # Import socket module
import time


keep_trying_to_connect = True

while keep_trying_to_connect:
    
    port = 5556    # Reserve a port for your service every new transfer wants a new port$
    
    s = socket.socket()        # Re-Create a socket object
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)     # the SO_REUSEADDR flag that tells the kernel to reuse a local socket in TIME_WAIT state, without waiting for its natural timeout to expire
    s.bind(('', port))
    s.listen(100)        # Now wait for client connection.
    print('Server listening....')
    
    while True:                
        conn, addr = s.accept()     # Establish connection with client.
        print("Got connection from: ", addr)
    
        data = conn.recv(1024)
        print('Received Data From Edge:  ', data.decode())
        if len(data) == 0:
            break
        
        filename = 'air_pressure_data_' + str(int(time.time()))
        with open(filename, 'wb') as f:
            f.write(data)      # write data to a file
            confirm_msg = 'MsgFromCloud:  File Has Been Received Succesfully!'
            conn.send(confirm_msg.encode())
            print('Successfully get the file')


conn.close()
print('connection closed')

