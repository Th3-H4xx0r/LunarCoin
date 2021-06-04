#----- A simple TCP client program in Python using send() function -----

import socket

from Signatures import Signatures

import pickle

# Create a client socket
myPrivate, myPublic = Signatures().load_key('privateKey.pem')
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

 

# Connect to the server

clientSocket.connect(("localhost",5005));

 

# Send data to server

dataToSend =  b'send_user_balance_command:' + myPublic
data = pickle.dumps(dataToSend)

clientSocket.send(data);

 

# Receive data from server

dataFromServer = clientSocket.recv(1024);

 

# Print to the console

print(dataFromServer.decode());