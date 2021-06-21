# Imports
from connections import Connections
import socket
import pickle

from colorama import init 
from termcolor import colored 
from SocketUtil import SocketUtil
from progress.bar import Bar
import requests
import os
import random
import itertools, sys
import sys
import logging
import time

init()

# Global variables

BUFFER_SIZE = 65536

class BlockchainSyncUtil:

    def __init__(self):
        self.init = True

    '''
    def payMinerReward(self, public):

        # TODO: Work on adding miner reward

        minerNodesList = SocketUtil.getMinerNodes()

        bar = Bar('Processing miner reward transaction', max=len(minerNodesList))

        for i in range(len(minerNodesList)):
            try:

                #if(minerNodesList[i]['ip'] != ip and minerNodesList[i]['port'] != port):
                SocketUtil.sendObj(minerNodesList[i]['ip'], Tx, minerNodesList[i]['port'])

            except Exception as e:
                pass
                
            bar.next()
        
        bar.finish()



        print(colored("[MINER CORE] Paying validator reward", "yellow"))


'''
    def syncSpamManagementClock(self, ip, port):
        try:
            print(colored('[MINER CORE] Syncing spam management service.','cyan'))

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))

            dataToSend = b'sync_spam_management'
            data = pickle.dumps(dataToSend)
            s.send(data)

            # Gets the bytes length of blockchain


            try:
                data = b''

                packet = s.recv(BUFFER_SIZE)

                

                data += packet
                #print("Got packet chain size")

                syncData = pickle.loads(data)

                print(syncData)

                s.close()

                if(syncData != None):
                    return syncData['secondsLeft'], syncData['walletsList']

                else:
                    return None, None

            
            except Exception as e:
                print("Error with getting spam management sync data")
                return None, None
        
 

        except Exception as e:
            print(colored('[MINER CORE] Error with connecting to an validator node for spam management sync data: ' + str(e),'cyan'))

        
        return None, None


    def sendBlockchain(self, socket, blockchain):

        data = None

        try:
            #with open('Blockchain/blockchain.dat', 'rb') as handle:


            data = blockchain

            dataSend = pickle.dumps(data)

            blockchainLen = sys.getsizeof(dataSend)

            print("Bytes size of blockchain: " + str(blockchainLen))


            socket.send(pickle.dumps('chain_length:' + str(blockchainLen))) # Sends the initial length of blockchain

            #print("Send chain size to node")

            time.sleep(2)

            socket.send(dataSend) # Sends the blockchain
            socket.close()

        
        except Exception as e:

            print("Error with sending blockchain: " + str(e))

            dataSend = pickle.dumps(None)

            socket.send(dataSend)
            socket.close()

    def getNodes(self, net):

        nodes = Connections().getNetworkNodes()

        rtnData = None

        for node in nodes:
            try:
                r = requests.get(node + '/validator/getNodes?network=' + str(net))

                data = r.json()

                rtnData = data

                break


            except Exception as e:
                rtnData =  None

        return rtnData

        
    def getRandomNode(self, currentID, data):

        try:

            if(data['status'] == 'success'):
                nodes = data['data']
            

                for node in nodes: # Takes out current node from list
                    if(node['nodeID'] == currentID):
                        nodes.remove(node)

                
                if(len(nodes) > 0): 

                    nodeIndex = random.randint(0, len(nodes) - 1)

                    selectedNode = nodes[nodeIndex]

                    ip = selectedNode['ip']
                    port = selectedNode['port']

                    #print(ip)

                    #print(port)

                    return ip, int(port), selectedNode
                    
                else: # If list is empty
                    return True, True, True


            else: # Fetch failed
                if(data['message'] == 'no such table: nodes'): # If this is the first online node
                    return True, True, True
                
                else:
                    return None, None, None

        except Exception as e: # Fetch error
            print("Error with getting nodes: " + str(e))
            return None, None, None



    def chainInitSync(self, ip, port):

        try:
            print(colored('[MINER CORE] Syncing blockchain.','cyan'))

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))

            dataToSend = b'blockchain_init_sync'
            data = pickle.dumps(dataToSend)
            s.send(data)

            # Gets the bytes length of blockchain


            try:
                data = b''

                packet = s.recv(BUFFER_SIZE)

                

                data += packet
                #print("Got packet chain size")

                blockchainLength = pickle.loads(data)

                blockchainLength = int(blockchainLength[blockchainLength.find(":") + 1:])

                #print(blockchainLength)

                try:

                    data = b''

                    PACKET_SIZE_RECV = 65569


                    bar = Bar('Downloading blockchain', max=(int(blockchainLength/PACKET_SIZE_RECV) + 1)) # Adds one to avoid zero-division error

                    #spinner = itertools.cycle(['-', '/', '|', '\\'])

                    while True:
                        packet = s.recv(BUFFER_SIZE)

                        if not packet: break
                        
                        # Shows spinner for packet loading

                        #sys.stdout.write(next(spinner))   # write the next character
                        #sys.stdout.flush()                # flush stdout buffer (actual character display)
                        #sys.stdout.write('\b')            # erase the last written char
                        
                        bar.next()

                        data += packet
                    
                    bar.finish()

                    #print(data)

                    dataLoaded = pickle.loads(data)

                    #print(dataLoaded)

                    #print(dataLoaded.current_transactions)

                    try:

                        handle = open('Blockchain/blockchain.dat', 'wb')

                        pickle.dump(dataLoaded.chain, handle, protocol=pickle.HIGHEST_PROTOCOL)

                        handle.close()

                    
                    except Exception as e:

                        current_directory = os.getcwd()

                        final_directory = os.path.join(current_directory, r'Blockchain')
                        if not os.path.exists(final_directory):
                            os.makedirs(final_directory)
                                            
                        handle = open('Blockchain/blockchain.dat', 'wb')

                        pickle.dump(dataLoaded.chain, handle, protocol=pickle.HIGHEST_PROTOCOL)

                        handle.close()

                        print(colored('[MINER CORE] Blockchain dir does not exist, crating directory.','cyan'))


                    print(colored('[MINER CORE] Successfully synced the blockchain','cyan'))


                    return True, dataLoaded.current_transactions


                    #blockVerifyList.append(data.decode())

            
                except Exception as e1:
                    logging.exception('message')
                    
                    print(colored('[MINER CORE] Error with blockchain sync has occured: ' + str(e1),'cyan'))
                
                
                s.close()

            
            except Exception as e:
                print("Error with getting blockchain length")


                


        except Exception as e:
            print(colored('[MINER CORE] Error with connecting to an validator node: ' + str(e),'cyan'))

        
        return False, None

    def sendRecievedBlock(self, blockRecv, blockchain, socket):
        lastBlock = blockchain.last_block_blockchain()

        data = pickle.dumps(lastBlock)
        socket.send(data)
        socket.close()

        print("Sent miner node current version of block")




