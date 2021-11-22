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
from pymongo import MongoClient

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
                print("Error with getting spam management sync data: " + str(e))
                return None, None
        
 

        except Exception as e:
            print(colored('[VALIDATOR CORE] Error with connecting to an validator node for spam management sync data: ' + str(e),'cyan'))

        
        return None, None


    def sendInvoicePool(self, socket, blockchainObj, previousChunkID=None):

        try:

            for i in range(10):

                data,lastID = blockchainObj.get_invoices_sync_util(5, previousChunkID)

                print("=================================================================")
                print(data)
                print(lastID)

                socket.sendall(pickle.dumps({"poolChunk": data, "lastID": lastID}))

                previousChunkID = lastID

                print("Sent invoice pool chunk")
                print("=================================================================")

            return 0
        
        except Exception as e:

            print("Error with sending invoice pool chunk: " + str(e))

            dataSend = pickle.dumps(None)

            socket.send(dataSend)
            socket.close()

            return 0
    

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
            return None
        
        except Exception as e:

            print("Error with sending block: " + str(e))
            #print(traceback.format_exc())
            dataSend = pickle.dumps(None)
            socket.send(dataSend)
            socket.close()
            return None
    
    def sendBlockchain_BLOCK_HASH_HEADERS(self, socket, blockchainObj, BLOCK_HEIGHT_START, BLOCK_HEIGHT_END):

        BLOCK_HEIGHT_START = int(BLOCK_HEIGHT_START)
        BLOCK_HEIGHT_END = int(BLOCK_HEIGHT_END)

        try:
            block_hashes = []
            for i in range(BLOCK_HEIGHT_START, BLOCK_HEIGHT_END+1):
                block = blockchainObj.getBlock(i)
                del block['_id']
                computedHash = blockchainObj.computeHash(block)
                block_hashes.append({"height": i, "hash": computedHash})
            socket.sendall(pickle.dumps(block_hashes)) 
            socket.close()
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            return None
        
        except Exception as e:

            print("Error with sending block: " + str(e))
            #print(traceback.format_exc())
            dataSend = pickle.dumps(None)
            socket.send(dataSend)
            socket.close()
            return None

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

    async def invoicePoolSync(self, fullNodesList):
        '''
        # Invoice Pool Initial Sync
        '''

        # Generates random node to fetch pool
        
        ip, port, nodeDataJSON = BlockchainSyncUtil().getRandomNode(None, fullNodesList)

        print(colored('[VALIDATOR CORE] Syncing invoices pool.','cyan'))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        #s.setblocking(0)
        dataToSend = b'invoice_pool_init_sync'
        data = pickle.dumps(dataToSend)
        s.sendall(data)

        try:
            dataTemp = b''

            for i in range(10):

                while True:
                    blockPacket = s.recv(BUFFER_SIZE)
                    dataTemp += blockPacket

                    if not blockPacket: break
                    
                poolChunkData = pickle.loads(dataTemp)
                print(poolChunkData)

        
        except Exception as e:
            print("Failed to recieve pool: " + str(e))







    async def chainInitSync(self, ip, port, fullNodesList, minerID):

        #print(fullNodesList)
        #print("======================================================")

        '''
        # Blockchain initial sync

        -  Current blockchain is checked for missing blocks and blockcount
        -  Add more
        '''

        # Checks current blockchain

        badHashBlocks=[]
        client=MongoClient('localhost')
        db=client.LunarCoin
        currentChainHeight=db.Blockchain.estimated_document_count()
        missingBlocks=[]
        blockHostRecvList={}
        fullNodesListTemp=fullNodesList

        # Finds missing blocks

        print("LOCAL CHAIN HEIGHT: " + str(currentChainHeight))

        for i in range(currentChainHeight):
            blockData = BlockchainMongo.getBlockStatic(db, i)  
            if not blockData: missingBlocks.append(i)
            
        try:
            # Requests for blockchain sync
            print(colored('[VALIDATOR CORE] Syncing blockchain.','cyan'))
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
            #s.setblocking(0)
            dataToSend = b'blockchain_init_sync'
            data = pickle.dumps(dataToSend)
            s.sendall(data)

            # Gets the block length of most recent blockchain from peer
            try:
                data = b''
                packet = s.recv(BUFFER_SIZE)
                data += packet
                blockchainLength = pickle.loads(data)
                s.close()
                blockchainLength = int(blockchainLength[blockchainLength.find(":") + 1:])

                if(blockchainLength == 0):
                    blockchainLength = 1
                breakUpIterations = int((blockchainLength-(blockchainLength%100))/100) + 1
                iterIndex = 0
                #print("Got packet chain size: " + str(blockchainLength))

                try:
                # Delete current blockchain if sync is found
                    #print("Deleting current blockchain...")
                    #BlockchainMongo.deleteBlockchainStatic()

                    try:
                        #print("Waiting to get blockchain...")

                        bar = Bar('Downloading blockchain', max=(int(breakUpIterations))) # Adds one to avoid zero-division error
                        for i in range(breakUpIterations): # Goes through each block chunk

                            try:
                                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                s.connect((ip, port))
                                blockDataTemp = b''
                                dataToSend = None

                                missingBlockInRange = False
                                startIdx, endIdx= iterIndex, iterIndex + 99

                                #print(missingBlocks)

                                for missingBlockIndex in missingBlocks:
                                    if(missingBlockIndex >= iterIndex and missingBlockIndex <= endIdx):
                                        missingBlockInRange = True

                                if(missingBlockInRange):
                                    dataToSend = b'block_sync:' + bytes(str(iterIndex), 'utf-8') + b'-' + bytes(str(iterIndex + 99), 'utf-8')
                                    # Delete current blocks in this range
                                    for i in range(startIdx, endIdx + 1):
                                        db.Blockchain.delete_one({'block_height': i})

                                #print("######################")
                                #print(currentChainHeight)
                                #print(startIdx)
                                #print(endIdx)
                                #print((missingBlockInRange == False and currentChainHeight >= startIdx and currentChainHeight >= endIdx))
                                #print("######################")
                                
                                if(missingBlockInRange == False and currentChainHeight >= startIdx and currentChainHeight >= endIdx):
                                    # Requests just block hash headers to verify current block integrity
                                    dataToSend = b'blockchain_hash_header_sync:' + bytes(str(iterIndex), 'utf-8') + b'-' + bytes(str(iterIndex + 99), 'utf-8')
                                    print("SEND HASHES")
                                else:
                                    dataToSend = b'block_sync:' + bytes(str(iterIndex), 'utf-8') + b'-' + bytes(str(iterIndex + 99), 'utf-8')
                                    missingBlockInRange = True
                                    # Delete current blocks in this range
                                    for i in range(startIdx, endIdx + 1):
                                        db.Blockchain.delete_one({'block_height': i})

                                #print(missingBlockInRange)
                                
                                #print(dataToSend)

                                iterIndex+=100
                                data = pickle.dumps(dataToSend)
                                s.sendall(data)

                                #fullNodesListTemp.remove()

                                while True:
                                    blockPacket = s.recv(BUFFER_SIZE)
                                    blockDataTemp += blockPacket

                                    if not blockPacket: break
                                    
                                blockData = pickle.loads(blockDataTemp)
                                #else: # Adds block to the local blockchain

                                badHashInBlockChunk = False

                                chunkGetIteration = 1

                                # Logs where the block chunk came from
                                blockHostRecvList[f'{iterIndex-100}:{iterIndex-1}-' + str(chunkGetIteration)] = {"ip": ip, "port": port}

                                for block in blockData:
                                    try:
                                        if(block != None):
                                            if(missingBlockInRange): # If there are missing blocks in the range, or there are no blocks in this range
                                                BlockchainMongo.saveBlockStatic(block)
                                            else:
                                                #print(block)
                                                height = block['height']
                                                block_hash = block['hash']
                                                localBlock = BlockchainMongo.getBlockStatic(db, height)
                                                del localBlock['_id']
                                                getLocalBlockHash = BlockchainMongo.computeHash(localBlock)

                                                #print(height)

                                                if getLocalBlockHash == block_hash:
                                                    #print ("Hash of block " + str(height) + " matches with current chain")
                                                    pass
                                                else:
                                                    badHashBlocks.append(height)
                                                    badHashInBlockChunk = True
                                                    print("BAD HASH")
                                        
                                    except Exception as e:
                                        print("ERROR: " + str(e))
                                        pass
                                
                                if(badHashInBlockChunk):

                                    retryIndex = 0

                                    while retryIndex < 5: # Upto five retries of redowloading blockchain

                                        retrialError = False
                                        s.close() # Closes concurrent connection
                                        print("Bad block hash verification in current chunk. Redownloading chunk of blocks")

                                        '''
                                        # REGETS THE BLOCK TO GET VALID HASHES
                                        # IMPLEMENTATION BELOW
                                        '''
                                        
                                        dataToSend = b'block_sync:' + bytes(str(iterIndex-100), 'utf-8') + b'-' + bytes(str(iterIndex-1), 'utf-8')
                                        #print(dataToSend)
                                        data = pickle.dumps(dataToSend)

                                        # Reconnects to node
                                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                        s.connect((ip, port))
                                        s.sendall(data)

                                        #print("Sent for redownload")

                                        blockDataTemp = b''

                                        while True:
                                            blockPacket = s.recv(BUFFER_SIZE)
                                            blockDataTemp += blockPacket

                                            if not blockPacket: break
                                        
                                        #print("Got redownload")

                                        # Delete the data for this chunk
                                        for i in range(startIdx, endIdx + 1):
                                            db.Blockchain.delete_one({'block_height': i})

                                        blockDataNew = pickle.loads(blockDataTemp)
                                        #else: # Adds block to the local blockchain

                                        badHashInBlockChunk = False

                                        chunkGetIteration = 1

                                        #print(blockDataTemp)

                                        # Logs where the block chunk came from
                                        blockHostRecvList[f'{iterIndex-100}:{iterIndex-1}-' + str(chunkGetIteration)] = {"ip": ip, "port": port}

                                        for block in blockDataNew:
                                            #print(block)
                                            try:
                                                if(block != None):
                                                    BlockchainMongo.saveBlockStatic(block)
                                            except Exception as e:
                                                print("ERROR: " + str(e))
                                                retrialError = True
                                                pass
                                        
                                        if(retrialError == False):
                                            break
                                        else:
                                            print("Error with trial to resync block chunk. Retrying...")
                                            retryIndex+=1 # Increments retry count
                                        
                                        # Communicates with another node to get next chunk (if avaliable) (Bandwidth load balancing)
                                        ip, port, nodeDataJSON = BlockchainSyncUtil().getRandomNode(minerID, fullNodesList)
                                        print("new node generated: " + str(ip) + ":" + str(port))

                                s.close()
                                bar.next()

                                # Communicates with another node to get next chunk (if avaliable) (Bandwidth load balancing)
                                ip, port, nodeDataJSON = BlockchainSyncUtil().getRandomNode(minerID, fullNodesList)
                                print("new node generated: " + str(ip) + ":" + str(port))

                            except Exception as e:
                                print("ERROR 1: " + str(e))

                        bar.finish()
                        s.close()

                        #print(blockHostRecvList)

                        #print("Blocks with bad hash: " + str(badHashBlocks)) # TODO: Implement

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




