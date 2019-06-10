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

from subprocess import call
import glob

from apscheduler.schedulers.background import BackgroundScheduler
import socket           # Import socket module

from time import sleep 


HOST = "localhost"
PORT = 4225
UID = "fGg" # UID of Air Pressure
log_file_name = '/home/basha/Desktop/FC_Project/fog_computing/edge/logfile'


cloud_host = "52.211.232.41"  #I p address that the TCPServer  is there 
cloud_port = 5556             # Reserve a port for your service every new transfer wants a new por$


def send_log_file_to_cloud():
    logfiles = [file for file in glob.glob('%s*' % log_file_name)]

    connected = True
    for file in logfiles:
        f = open(file,'rb')
        lines = f.read()
        f.close()
        try:
            s = socket.socket()             # Create a socket object
            s.connect((cloud_host, cloud_port))
            s.send(lines)
            print('Done sending')
            conf_msg = s.recv(1024)
            print(conf_msg.decode())
            mkdircdm = 'mkdir -p newlogfiles'
            call(mkdircdm.split())
            mvcmd = 'mv ' + file + ' newlogfiles/'
            call(mvcmd.split())
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
                    sleep(1)            


try:
    # set TimedRotatingFileHandler for root
    formatter = logging.Formatter('%(asctime)s %(message)s')
    # use very short interval for this example, typical 'when' would be 'midnight' and no explicit interval
    handler = TimedRotatingFileHandler(log_file_name, when="S", interval=8, backupCount=100)
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
    

# Callback function for air pressure callback
def cb_air_pressure(air_pressure):
    print("Air Pressure: " + str(air_pressure/1000.0) + " mbar")
    logger.info("|" + str(air_pressure/1000.0))

if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    b = BrickletBarometer(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd

    # Register air pressure callback to function cb_air_pressure
    b.register_callback(b.CALLBACK_AIR_PRESSURE, cb_air_pressure)

    # Note: The air pressure callback is only called every 500 ms
    # if the air pressure has changed since the last call!
    b.set_air_pressure_callback_period(1000)

    # Send file to cloud
    sched = BackgroundScheduler()
    sched.add_job(send_log_file_to_cloud, 'interval', seconds = 10, max_instances=1000)
    sched.start()
    
    input("Press key to exit\n") # Use input() in Python 3
    ipcon.disconnect()
