#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 23:56:22 2019

@author: basha
"""


import socket    # Import socket module
import time
from statistics import mean
from decimal import Decimal


def get_air_pressure_stats(listofvalues):
    air_pressure_list = []
    for val in listofvalues:
        air_pressure_list.append(float(val[1]))
    mean_val = round(Decimal(mean(air_pressure_list)), 3)

    return mean_val


def create_prediction_msg(filename):
    listofvalues = []
    with open(filename, 'r') as file:
        for line in file:
            listofvalues.append(line.split('|'))
    mean_val = get_air_pressure_stats(listofvalues)
    return_msg = get_msg(mean_val)
        
    return return_msg


def get_msg(mean_val):
    return_msg = 'Unknown Pressure Value!'
    if mean_val >= 1086:
        return_msg = 'Highest Ever Recorded'
    elif mean_val >= 1030:
        return_msg = 'Strong High Pressure System'
    elif mean_val >= 1013:
        return_msg = 'Average Sea Level Pressure'
    elif mean_val >= 1000:
        return_msg = 'Typical Low Pressure System'
    elif mean_val >= 980:
        return_msg = 'CAT 1 Hurricane or a very intense mid-latitude cyclone'
    elif mean_val >= 950:
        return_msg = 'CAT 3 Hurricane'
    elif mean_val >= 870:
        return_msg = 'Lowest Ever Recorded (not including tornadoes)'
        
    return return_msg

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
            
        print('Successfully get the file')
        return_msg = create_prediction_msg(filename)
        conn.send(return_msg.encode())
        print("Prediction message has been sent sussessfully!")

conn.close()
print('connection closed')

