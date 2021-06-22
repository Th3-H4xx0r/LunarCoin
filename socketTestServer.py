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

#serversocket.setblocking(0)
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

    timeout = 0.5


    #make socket non blocking
    clientsocket.setblocking(0)
    
    #total data partwise in an array
    total_data=[];
    data='';
    
    #beginning time
    begin=time.time()
    while 1:
        #if you got some data, then break after timeout
        if total_data and time.time()-begin > timeout:
            break
        
        #if you got no data at all, wait a little longer, twice the timeout
        elif time.time()-begin > timeout*2:
            break
        
        #recv something
        try:
            data = clientsocket.recv(8192)
            if data:
                total_data.append(data)
                #change the beginning time for measurement
                begin=time.time()
            else:
                #sleep for sometime to indicate a gap
                time.sleep(0.1)
        except:
            pass
    
        #join all parts to make final string
        all_data = b''.join(total_data)

    #for i in range(10):
    #packet = clientsocket.recv(10485760)
    print(sys.getsizeof(all_data))

        #if not packet: break
    #print(packet)

    #print(sys.getsizeof(packet))

        ##if not packet:
            #clientsocket.close()
            #break
        #if not packet: break
    #all_data = all_data + packet
    
    #time.sleep(1)
    returnData = pickle.loads(all_data)

    #print(returnData)

    #time.sleep(1)

    #time.sleep(2)
    clientsocket.send(pickle.dumps('1000'))

    clientsocket.close()