#----- A simple TCP client program in Python using send() function -----

import socket

from Signatures import Signatures

import pickle
import threading
import time

# Create a client socket
#myPrivate, myPublic = Signatures().load_key('privateKey.pem')



# Connect to the server


nodes = [["localhost",8092], ["localhost",8091]]

x = '''
import time 

x = 1

def service():
    global x
    x = x + 1
    while True:
        x = x * x
        time.sleep(0.1)
        print(x)
'''

for node in nodes:
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    clientSocket.connect((node[0],node[1]));
    clientSocket.sendall(pickle.dumps(x))
    clientSocket.close()
