# Fog Computing Prototyping
From Cloud to Fog - Fog Computing Prototype

### Project Description:
- Setup an emulator for TinkerForge devices.
- Choose Air Pressure device from the list of available devices.
- Send data from Barometer device every 1000ms to local machine (Edge).
- Receive data from Barometer device and save it to log file using logging library. [2]
- Create a socket object to build a connection with the EC2 machine using a specific port, in case of connection failure, the application keeps trying to recreate the socket object and build the connection every one second.
- Every 15 seconds, close the log file, name it with the current unix timestamp, then send its content using python socket to the EC2 instance (Cloud).
- At Cloud, we create a socket object and bind to any requests coming to the same port which we specified before, then the EC2 starts to listen to requests from Edge. 
- Once the EC2 receives a request from Edge, the connection is established, then it starts to write the received data to a file, then name the file with the current unix timestamp, then closes the file.
- Then, at the Cloud we compute the mean value of air pressure values within the file, then sends a forecast prediction message to Edge. [3]
- At Edge, once it receives a confirmation message, it deletes the log file to free some storage due to the storage limitation on Edge.
- In case of internet disconnection between Edge and Cloud, both of them keep working without any corruption because at Cloud we use the SO_REUSEADDR flag that tells the kernel to reuse a local socket in TIME_WAIT state, without waiting for its natural timeout to expire, with this simple flag added to the cloud socket, we prevent the socket death and keep connecting to the same socket which binds to Edge socket. [4]

### Conclusion
Overall, after we have implemented this prototype by ourselves, we have learned how fog computing technology can solve the current issues of cloud architecture with the world of IoT and we got a clear view about the challenges of applying this technology in real-world scenario.

Finally, After testing our application, we found that we have fulfilled all the requirements:
- Used local machine and build connection with cloud machine.
- Used TinkerForge emulator and collect data from (emulated) IoT device.
- Data has been transmitted multiple times per minute between edge and cloud.
- Internet disconnection doesn't affect the functionality or causes loss of data.

### References
- [1] Tinkerforge Emulator: https://github.com/PlayWithIt/TFStubserver 
- [2] Logging facility for Python: https://docs.python.org/3/library/logging.html
- [3] Air pressure on weathercasts : http://www.theweatherprediction.com/habyhints2/410/ 
- [4] Socket - low level networking interface: https://docs.python.org/3/library/socket.html#example

