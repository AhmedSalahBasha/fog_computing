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
import os
import psutil



def get_air_pressure_stats(listofvalues):
    air_pressure_list = []
    for val in listofvalues:
        air_pressure_list.append(float(val[1]))
    mean_val = round(Decimal(mean(air_pressure_list)), 3)
    return mean_val


def create_prediction_msg(filename):
    i = 0
    listofvalues = []
    with open(filename, 'r') as file:
        for line in file:
            listofvalues.append(line.split('|'))
    mean_val = get_air_pressure_stats(listofvalues)
    return_msg = get_msg(mean_val) 
    return_msg = str(i) + ' - ' + return_msg
    i += 1
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
        return_msg = 'Lowest Ever Recorded' 
    return return_msg


def has_handle(fpath):
    for proc in psutil.process_iter():
        try:
            for item in proc.open_files():
                if fpath == item.path:
                    return True
        except Exception:
            pass
    return False

keep_trying_to_connect = True
while keep_trying_to_connect:
    port = 5556    # Reserve a port for your service every new transfer wants a new port$
    s = socket.socket()        # Re-Create a socket object
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)     # the SO_REUSEADDR flag that tells the kernel to reuse a local socket in TIME_WAIT state, without waiting for its natural timeout to expire
    s.bind(('', port))
    s.listen(100)   # Now wait for client connection.
    print('Server listening....')       
    while True: 
        conn, addr = s.accept()     # Establish connection with client.
        print("Got connection from: ", addr)
        data = conn.recv(1024)
        print('Received Data From Edge:  ', data.decode())
        if len(data) == 0:
            break
        mkdircdm = 'mkdir -p received_files'
        os.system(mkdircdm)
        filename = '/home/ubuntu/fogcomputing/socket_test/received_files/air_pressure_data_' + str(int(time.time()))
        f = open(filename, 'wb')
        f.write(data)      # write data to a file
        f.close()
        time.sleep(0.5)
        if not has_handle(filename):
            print('Successfully get the file at:  ', time.ctime())
            return_msg = create_prediction_msg(filename)
            conn.send(return_msg.encode())
            print("Prediction message has been sent sussessfully!")


conn.close()
print('connection closed')

