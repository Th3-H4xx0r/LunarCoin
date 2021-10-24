import socket
import pickle
import time
from time import sleep
import sys
import threading
import ComputeService
import ctypes
import os
import multiprocessing



process = None
mainProccess = []


def stopProcess():
    global mainProccess

    for prc in mainProccess:
        prc.terminate()
        print("Stopped process")

def socketServer():
    global mainProccess
    global process
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

        try:
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
            

            while True:
                try:
                    data = clientsocket.recv(8192)
                    if data:
                        total_data.append(data)
                    else:
                        #sleep for sometime to indicate a gap
                        break
                except:
                    pass

            #join all parts to make final string
            all_data = b''.join(total_data)

            #for i in range(10):


                #if not packet: break
            #print(packet)

            #print(sys.getsizeof(packet))

                ##if not packet:
                    #clientsocket.close()
                    #break
                #if not packet: break
            #all_data = all_data + packet
            
            #time.sleep(1)
            try:

                print(mainProccess)
                returnData = pickle.loads(all_data)
                print("UPDATE COMMAND RECEIVED " + str(returnData))
                #t1.raise_exception()
                #t1.join()

                stopProcess()
                #mainProccess.terminate()


                with open("ComputeService.py", 'w+') as file:
                    code = returnData
                    
                    xxx= f'''
import time 

def service():
    while True:
        {returnData}
        time.sleep(2)
            
        '''

                    file.seek(0)
                    file.write(code)
                    file.close()

                # Restart thread
                time.sleep(2)
                print("Restarting thread")

                process = multiprocessing.Process(target=func)
                process.start()
                mainProccess.append(process)

                #t1 = thread_with_exception('Thread 1')
                #t1.start()
            
            except Exception as e:
                print("EXCEPTION: " + str(e))
                pass

            #print(returnData)

            #time.sleep(1)

            #time.sleep(2)
            #clientsocket.send(pickle.dumps('1000'))

            clientsocket.close()
        
        except Exception as e:
            print("EXCEP: " + str(e))



def func():
    ComputeService.service()

#t1 = thread_with_exception('Thread 1')
#t1.start()

if __name__ == '__main__':

    try:
        process = multiprocessing.Process(target=func)
        process.start()
        mainProccess.append(process)

        print(mainProccess)

    except Exception as e:
        print("Cant start thread: " + str(e))

    socketThread = multiprocessing.Process(target=socketServer)
    socketThread.start()

