import socket
import pickle
import time
from time import sleep
import sys

# create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#serversocket.settimeout(5)
# bind the socket to a public host, and a well-known port
serversocket.bind(('localhost', 8092))
# become a server socket
serversocket.listen(1)

serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 10485760)  

while True:
    # accept connections from outside
    (clientsocket, address) = serversocket.accept()
    # now do something with the clientsocket
    # in this case, we'll pretend this is a threaded server
    #ct = client_thread(clientsocket)
   # ct.run()

    #clientsocket.setblocking(0)

    all_data = b''

    #while True:

    #for i in range(10):
    packet = clientsocket.recv(10485760)
    print(sys.getsizeof(packet))

        #if not packet: break
    #print(packet)

    #print(sys.getsizeof(packet))

        ##if not packet:
            #clientsocket.close()
            #break
        #if not packet: break
    all_data = all_data + packet
    
    #time.sleep(1)
    returnData = pickle.loads(all_data)

    #print(returnData)

    #time.sleep(1)

    #time.sleep(2)
    clientsocket.send(pickle.dumps('1000'))

    clientsocket.close()