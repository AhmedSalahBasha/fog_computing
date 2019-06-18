#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 14:20:03 2019

@author: basha
"""


from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_barometer import BrickletBarometer

import logging
from logging.handlers import TimedRotatingFileHandler

import glob
import psutil

from apscheduler.schedulers.background import BackgroundScheduler
import socket           # Import socket module

import time 
import os


HOST = "localhost"
PORT = 4225
UID = "fGg" # UID of Air Pressure
log_file_name = '/home/basha/Desktop/FC_Project/fog_computing/edge/logfile'


cloud_host = "34.244.127.77"  #Ip address that the TCPServer is there 
cloud_port = 5556             # Reserve a port for your service every new transfer wants a new por$

conf_msgs_list = []
sent_msgs_list = []

def has_handle(fpath):
    for proc in psutil.process_iter():
        try:
            for item in proc.open_files():
                if fpath == item.path:
                    return True
        except Exception:
            pass
    return False


def send_log_file_to_cloud():
    logfiles = [file for file in glob.glob('%s*' % log_file_name)]
    connected = True
    try:
        for file in logfiles:
            if not has_handle(file):
                f = open(file,'rb')
                lines = f.read()
                f.close()
                s = socket.socket()             # Create a socket object
                s.connect((cloud_host, cloud_port))
                s.send(lines)
                sent_msgs_list.append(lines)
                print('Done sending at:  ', time.ctime())
                conf_msg = s.recv(1024)
                conf_msgs_list.append(conf_msg)
                print('===>>> MsgFromCloud:  ' + conf_msg.decode())
                mkdircdm = 'mkdir -p sent_files'
                os.system(mkdircdm)
                mvcmd = 'mv ' + file + ' sent_files/'
                os.system(mvcmd)
                logfiles.remove(file)
    except socket.error:
        #set connection status and recreate socket
        connected = False
        s = socket.socket() 
        print("connection lost... reconnecting")
        while not connected:
            #attempt to reconnect, otherwise sleep for 1 seconds
            try:
                s.connect((cloud_host, cloud_port))
                connected = True
                print("re-connection successful")
            except socket.error:
                time.sleep(1)
    finally:
        print('================================')
        print('[1] Number of Sent Files to Cloud:  ', len(sent_msgs_list))
        print('[2] Number of Received Messages From Cloud:  ', len(conf_msgs_list))

    

# Callback function for air pressure callback
def cb_air_pressure(air_pressure):
    print("Air Pressure: " + str(air_pressure/1000.0) + " mbar")
    logger.info("|" + str(air_pressure/1000.0))

if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    b = BrickletBarometer(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    
    # create logger object
    try:
        # set TimedRotatingFileHandler for root
        formatter = logging.Formatter('%(asctime)s %(message)s')
        # use very short interval for this example, typical 'when' would be 'midnight' and no explicit interval
        handler = TimedRotatingFileHandler(log_file_name, when="S", interval=4, backupCount=100)
        handler.setFormatter(formatter)
        logger = logging.getLogger('root') # or pass string to give it a name
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    except KeyboardInterrupt:
        # handle Ctrl-C
        logging.warn("Cancelled by user")
    except Exception as ex:
        # handle unexpected script errors
        logging.exception("Unhandled error\n{}".format(ex))
        raise
    finally:
        # perform an orderly shutdown by flushing and closing all handlers.
        logging.shutdown()
    
    # Register air pressure callback to function cb_air_pressure
    b.register_callback(b.CALLBACK_AIR_PRESSURE, cb_air_pressure)

    # Note: The air pressure callback is only called every 500 ms
    # if the air pressure has changed since the last call!
    b.set_air_pressure_callback_period(1000)

    # Send file to cloud
    sched = BackgroundScheduler()
    sched.add_job(send_log_file_to_cloud, 'interval', seconds = 5, max_instances=1000)
    sched.start()
    

    input("Press key to exit\n") # Use input() in Python 3
    ipcon.disconnect()