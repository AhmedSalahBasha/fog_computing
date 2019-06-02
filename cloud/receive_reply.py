import zmq


PORT = "5556"
context = zmq.Context()
print("Waiting Message From Client...")

socket = context.socket(zmq.REP)
socket.bind("tcp://*:%s" % PORT)


while True:
    #Wait for next request from client
    message = socket.recv()
    print("Message From EDGE: ", message)
    #time.sleep (1)
    socket.send_string("Confirmation Message From Server")



