#----- A simple TCP client program in Python using send() function -----

import socket

from Signatures import Signatures

import pickle
import time

# Create a client socket
#myPrivate, myPublic = Signatures().load_key('privateKey.pem')
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

 

# Connect to the server

clientSocket.connect(("localhost",8092));
#clientSocket.setblocking(0)
#clientSocket.settimeout(5)
 

# Send data to server

dataToSend =  b'send_user_balance_command:sadfasdfasdf' * 1024 * 100
data = pickle.dumps(dataToSend)

clientSocket.send(data);
#clientSocket.send(b'')

#clientSocket.close()



 
#time.sleep(2)
# Receive data from server
#time.sleep(1)
dataFromServer = clientSocket.recv(1024);

 

# Print to the console

print(pickle.loads(dataFromServer));

clientSocket.close()