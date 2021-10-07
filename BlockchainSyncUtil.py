# Imports
from BlockchainMongo import BlockchainMongo
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
import traceback
import sys

from datetime import datetime

init()

# Global variables

BUFFER_SIZE = 6553611

class BlockchainSyncUtil:

    def __init__(self):
        self.init = True

    '''
    def payMinerReward(self, public):

        # TODO: Work on adding validator reward

        validatorNodesList = SocketUtil.getMinerNodes()

        bar = Bar('Processing validator reward transaction', max=len(validatorNodesList))

        for i in range(len(validatorNodesList)):
            try:

                #if(validatorNodesList[i]['ip'] != ip and validatorNodesList[i]['port'] != port):
                SocketUtil.sendObj(validatorNodesList[i]['ip'], Tx, validatorNodesList[i]['port'])

            except Exception as e:
                pass
                
            bar.next()
        
        bar.finish()



        print(colored("[VALIDATOR CORE] Paying validator reward", "yellow"))


'''
    def syncSpamManagementClock(self, ip, port):
        try:
            print(colored('[VALIDATOR CORE] Syncing spam management service.','cyan'))

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
            print(colored('[VALIDATOR CORE] Error with connecting to an validator node for spam management sync data: ' + str(e),'cyan'))

        
        return None, None


    def sendBlockchain_HEADER(self, socket, blockchainObj):

        try:

            height = blockchainObj.get_current_block_length()

            socket.sendall(pickle.dumps('chain_length:' + str(height))) # Sends the initial length of blockchain

            #print("Sent chain length")

            return 0

        
        except Exception as e:

            print("Error with sending blockchain: " + str(e))

            dataSend = pickle.dumps(None)

            socket.send(dataSend)
            socket.close()
    
    def sendBlockchain_BLOCK(self, socket, blockchainObj, BLOCK_HEIGHT_START, BLOCK_HEIGHT_END):

        BLOCK_HEIGHT_START = int(BLOCK_HEIGHT_START)
        BLOCK_HEIGHT_END = int(BLOCK_HEIGHT_END)

        try:

            blocks = []

            for i in range(BLOCK_HEIGHT_START, BLOCK_HEIGHT_END+1):
                block = blockchainObj.getBlock(i)
                blocks.append(block)

            socket.sendall(pickle.dumps(blocks)) 
            socket.close()

            
            now = datetime.now()

            current_time = now.strftime("%H:%M:%S")
            #print("Sent block with height: " + str(block['block_height']) + " At time: " + str(current_time))
        
            return 0

        
        except Exception as e:

            print("Error with sending block: " + str(e))
            #print(traceback.format_exc())

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



    async def chainInitSync(self, ip, port):

        
        #TODO: Verify blockchain integrity after sync

        try:

            # Requests for blockchain sync
            print(colored('[VALIDATOR CORE] Syncing blockchain.','cyan'))

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))

            #s.setblocking(0)

            dataToSend = b'blockchain_init_sync'
            data = pickle.dumps(dataToSend)
            s.sendall(data)



            # Gets the block length of blockchain

            try:
                data = b''

                packet = s.recv(BUFFER_SIZE)

                data += packet


                blockchainLength = pickle.loads(data)

                s.close()

                #print("Got packet chain size 1: " + str(blockchainLength))

                #saveBlockStatic() takes 1 positional argument but 2 were given


                blockchainLength = int(blockchainLength[blockchainLength.find(":") + 1:])

                if(blockchainLength == 0):
                    blockchainLength = 1
                
                breakUpIterations = int((blockchainLength-(blockchainLength%100))/100) + 1

                iterIndex = 0

                                

                print("Got packet chain size: " + str(blockchainLength))

                try:
                # Delete current blockchain if sync is found
                    print("Deleting current blockchain...")

                    BlockchainMongo.deleteBlockchainStatic()

                    try:

                        print("Waiting to get blockchain.")


                        bar = Bar('Downloading blockchain', max=(int(breakUpIterations))) # Adds one to avoid zero-division error

                        

                        for i in range(breakUpIterations):
                            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            s.connect((ip, port))

                            blockDataTemp = b''
                            

                            dataToSend = None

                            dataToSend = b'block_sync:' + bytes(str(iterIndex), 'utf-8') + b'-' + bytes(str(iterIndex + 99), 'utf-8')
                            iterIndex+=100
                            
                            data = pickle.dumps(dataToSend)
                            s.sendall(data)
                            

                            while True:
                                blockPacket = s.recv(BUFFER_SIZE)
                                blockDataTemp += blockPacket

                                if not blockPacket: break
                                

                            blockData = pickle.loads(blockDataTemp)

                            
                            #else: # Adds block to the local blockchain


                            for block in blockData:
                                try:
                                    if(block != None):
                                        BlockchainMongo.saveBlockStatic(block)
                                    
                                except Exception as e:
                                    print("ERROR: " + str(e))
                            

                            s.close()

                            bar.next()

                        
                        bar.finish()
                        s.close()

                        print(colored('[VALIDATOR CORE] Successfully synced the blockchain','cyan'))

 

                        return True # TODO: Add current transactions to the newly synced blockchain

                
                    except Exception as e1:
                        #logging.exception('message')

                        #print(traceback.format_exc())
                        
                        print(colored('[VALIDATOR CORE] Error with blockchain sync has occured: ' + str(e1),'cyan'))
                
                
                    s.close()
            
                except Exception as e:
                    print("Error with deleteing current blockchain. Unable to proceed: " + str(e))



            
            except Exception as e:
                #print(traceback.format_exc())
                print("Error with getting blockchain length: " + str(e))


                


        except Exception as e:
            print(colored('[VALIDATOR CORE] Error with connecting to an validator node: ' + str(e),'cyan'))

        
        return False, None

    def sendRecievedBlock(self, blockRecv, blockchain, socket):
        lastBlock = blockchain.last_block_blockchain()

        data = pickle.dumps(lastBlock)
        socket.send(data)
        socket.close()

        print("Sent validator node current version of block")




