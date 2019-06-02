#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 14:25:02 2019

@author: basha
"""

HOST = "localhost"
PORT = 4225
PORT_SERVER = "5556"
UID = "fGg" # Change XYZ to the UID of your Barometer Bricklet


from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_barometer import BrickletBarometer
import zmq

context = zmq.Context()
print("Connecting to Server...")

# Callback function for air pressure callback
def cb_air_pressure(air_pressure):
    socket = context.socket(zmq.REQ)
    socket.connect ("tcp://52.211.232.41:%s" % PORT_SERVER)
    #print("Sending request...")
    #print("Air Pressure: " + str(air_pressure/1000.0) + " mbar")
    socket.send_string("Air Pressure: " + str(air_pressure/1000.0) + " mbar")
    # Get the reply.
    message = socket.recv()
    print("Reply From Cloud: ", message)

if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    b = BrickletBarometer(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected

    # Register air pressure callback to function cb_air_pressure
    b.register_callback(b.CALLBACK_AIR_PRESSURE, cb_air_pressure)

    # Set period for air pressure callback to 1s (1000ms)
    # Note: The air pressure callback is only called every second
    #       if the air pressure has changed since the last call!
    b.set_air_pressure_callback_period(500)

    input("Press key to exit\n") # Use input() in Python 3
    ipcon.disconnect()

