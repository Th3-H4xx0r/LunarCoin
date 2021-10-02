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


    def sendBlockchain(self, socket, blockchainObj):

        data = None

        try:

            height = blockchainObj.get_current_block_height()

            socket.send(pickle.dumps('chain_length:' + str(pickle.dumps(height)))) # Sends the initial length of blockchain

            time.sleep(2)

            # Sends the blockchain - block by block

            for i in range(height):
                block = blockchainObj.getBlock(i)
                socket.send(pickle.dumps(block)) 
                socket.close()
            
            socket.send(pickle.dumps('--BLOCKCHAIN END--')) 
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
                # Delete current blockchain if sync is found
                    print("Deleting current blockchain...")

                    BlockchainMongo().deleteBlockchainStatic()

                    try:

                        blockDataTemp = b''

                        bar = Bar('Downloading blockchain', max=(int(blockchainLength) + 1)) # Adds one to avoid zero-division error



                        while True:

                            while True:
                                packet = s.recv(BUFFER_SIZE)

                                if not packet: break
                                
                                blockDataTemp += packet
                            
                            blockData = pickle.loads(blockDataTemp)
                            
                            if(blockData == '--BLOCKCHAIN END--'):
                                break
                            
                            else: # Adds block to the local blockchain
                                BlockchainMongo().saveBlockStatic(blockData)
                                

                            bar.next()

                        
                        bar.finish()

                        print(colored('[MINER CORE] Successfully synced the blockchain','cyan'))


                        return True, [] # TODO: Add current transactions to the newly synced blockchain

                
                    except Exception as e1:
                        logging.exception('message')
                        
                        print(colored('[MINER CORE] Error with blockchain sync has occured: ' + str(e1),'cyan'))
                
                
                    s.close()
            
                except Exception as e:
                    print("Error with deleteing current blockchain. Unable to proceed")



            
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




