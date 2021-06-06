# Imports

#try:
import socket
import pickle
import select
import threading
from SocketUtil import SocketUtil
from Signatures import Signatures
from Blockchain import Blockchain
import sys
from colorama import init 
from termcolor import colored 
from pyngrok import ngrok
import json
import time

import os

import BlockchainSyncUtil as BlockchainSyncUtil

init()
# Global var
TCP_PORT = 6003
BUFFER_SIZE = 1024

CURRENT_BLOCK = None
NGROK_AUTH_TOKEN = None
MINER_ID = None

NGROK_IP = None
NGROK_PORT = None
NETWORK = None

walletTxFreq = {}

sys.setrecursionlimit(1000000)

def loadConfiguration():

    global NGROK_AUTH_TOKEN
    global MINER_ID
    global NETWORK

    try:
        with open('config.json', 'r') as file:
            data = json.load(file)

            try: # Checks if ngrokAuthToken exists

                NGROK_AUTH_TOKEN = data['ngrokAuthToken']

                # Checks if ngrokAuthToken is proper

                if(isinstance(NGROK_AUTH_TOKEN, str) != True):
                    print(colored("Error with loading config.json: key ngrokAuthToken is not of type string", "red"))
                    return False

            except Exception as e:
                print(colored("Error with loading config.json: key ngrokAuthToken does not exist", "red"))
                return False


            try: # Checks if minerID exists
                MINER_ID = data['minerID']

                
                if(isinstance(MINER_ID, str) != True): # Checks if minerID is proper
                    print(colored("Error with loading config.json: key minerID is not of type string", "red"))
                    return False

            except Exception as e:
                print(colored("Error with loading config.json: key minerID does not exist", "red"))
                return False
            

            try: # Checks if network exists
                NETWORK = data['network']

                
                if(isinstance(MINER_ID, str) and (NETWORK == "mainnet" or NETWORK == "testnet")): # Checks if network is proper
                    pass
                
                else: 
                    print(colored("Error with loading config.json: key network is not of type string or is not 'mainnet' or 'testnet'", "red"))
                    return False

            except Exception as e:
                print(colored("Error with loading config.json: key network does not exist", "red"))
                return False


            # If all values successfull load

            print(colored("[MINER CORE] Loaded Miner Configs from config.json", "green"))
            return True

    
    # Error with file loading
    except Exception as e:
        print(colored("Error with loading config.json or file does not exist: " + str(e), "red")) 
        return False


def runGrok():

    global db
    global MINER_ID
    global NGROK_IP
    global NGROK_PORT
    global NETWORK

    # 1sbjL6HgcrNZeVi61XPymtYEisD_xaXYnSwRckKbJiUmBfVg   ---  token for mcendercraftnetwork@gmail.com

    ngrok.set_auth_token(NGROK_AUTH_TOKEN) # token for krishnatechpranav@gmail.com
    tunnel = ngrok.connect(TCP_PORT, "tcp")
    print("Running ngrok connection server: " + str(tunnel.public_url))

    NGROK_IP, NGROK_PORT = SocketUtil.updateMinerIp(tunnel.public_url, MINER_ID, NETWORK)




def recvObj(socket, blockchainObj, syncUtil):

    new_sock = None

    try:
        inputs, outputs, errs = select.select([socket], [], [socket], 6)

        if socket in inputs:


            new_sock, addr = socket.accept()

            #print("Accepted a connection request from %s:%s"%(addr[0], addr[1]));

            all_data = b''

            #while True:
            data = new_sock.recv(BUFFER_SIZE)
            #if not data: break
            all_data = all_data + data
            
            returnData = pickle.loads(all_data)

            #print(returnData)

            #print(type(returnData))

            #print(returnData)

            #print(isinstance(returnData, Blockchain))

            if('blockchain_init_sync' in str(returnData)): # Get user balance and send to user
                print('Blockchain sync requested from miner: ' + str(addr[0]) + ":" + str(addr[1]))

                #block = returnData

                #BlockchainSyncUtil.verifyBlock()

                #BlockchainSyncUtil.sendRecievedBlock(block, blockchainObj, new_sock)

                syncUtil.sendBlockchain(new_sock, blockchainObj)

                return None
                



            if('send_user_balance_command' in str(returnData)): # Get user balance and send to user

                print(colored("[WALLET REQUEST] Wallet request for balance", "blue"))

                publicUser = ''

                #Blockchain.getUserBalance(publicUser)

                index = str(returnData).index(":")

                publicKey = returnData[index - 1:]

                userCurrentBalance = blockchainObj.getUserBalance(publicKey)

                #print("user balance: " +str(userCurrentBalance))

                new_sock.send(str(userCurrentBalance).encode('utf-8'))

                #print("Sent user the balance data")

                print(colored("[WALLET REQUEST ACCEPTED] Wallet request for balance sent to wallet", "blue"))


                #print("send_user_balance_command for public key: " + str(publicKey))
                return None
            
            else:
                return pickle.loads(all_data)
        else:
            return None
    
    except Exception as e:
        print(colored("[FATAL ERROR] Error recieving object from client: " + str(e), "red"))


#def sendBlockchain(ip, port):

'''
def verifyBlock(block, db):

    blockVerifyList = []

    ref = db.collection(u"Miner Nodes")

    docs = ref.stream()

    for doc in docs:
        dataToSend = block

        try:

            dataDoc = doc.to_dict()

            if(dataDoc['ip'] != NGROK_IP and dataDoc['port'] != NGROK_PORT):

                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((dataDoc['ip'], dataDoc['port']))
                data = pickle.dumps(dataToSend)
                s.send(data)

                print("sent to " + str(dataDoc['ip'] + ":" + str(dataDoc['port'])))

                try:

                    data = s.recv(BUFFER_SIZE)

                    blockVerifyList.append(data.decode())

                
                except Exception as e1:
                    print("Error with blockchain sync has occured: " + str(e1))

                s.close()
        
        except Exception as e:
            print("Error with sending block to other nodes: " + str(e))
    
    #print(blockVerifyList)
'''

def archiveServer(my_addr):

    #try:

        global tx_list
        global break_now
        global walletTxFreq

        blockchain = Blockchain()

        syncUtil = BlockchainSyncUtil.BlockchainSyncUtil()

        my_ip, my_port = my_addr
        # Open server connection
        server = SocketUtil.newServerConnection(my_ip, my_port)

        while True:
            newTx = recvObj(server, blockchain, syncUtil)

            if(newTx != None):
                #print(newTx)
                print(colored("[Share Recieved] Transaction share recieved - Validating...", "green"))

                util = SocketUtil()

                #print(newTx)

                if(newTx.public == 'mining_reward'):

                    print("Mining reward transaction")

                    blockchain.new_transaction(newTx.public, newTx.outputAddress, newTx.outputAmount)

                    newBlock = blockchain.goNewBlock()

                    if(newBlock):

                        blockchain.new_block() # Creates new block if block meets all requirements\\

                else:

                    #print("regular transaction")


                    addrSimplified = newTx.public

                    addrSimplified = addrSimplified.replace(b'-----BEGIN PUBLIC KEY-----\n', b'')
                    addrSimplified = addrSimplified.replace(b'\n-----END PUBLIC KEY-----\n', b'')

                    addrSimplified = str(addrSimplified, 'utf-8')

                    if (walletTxFreq.get(addrSimplified) != None):
                        walletTxFreq[addrSimplified] = walletTxFreq[addrSimplified] + 1
                    else:
                        walletTxFreq[addrSimplified] = 1

                    
                    if(walletTxFreq.get(addrSimplified) > 2000): # If wallet spams
                        print(colored("[Share Rejected] Wallet address is executing too many transactions", "yellow"))

                    else: # If wallet does not spam

                        #print(newTx)
                        valid = util.verifyTransaction(newTx, newTx.public)

                        userCurrentBalance = blockchain.getUserBalance(newTx.public)

                        
                        #print(userCurrentBalance)

                        if(userCurrentBalance >= newTx.outputAmount):

                            if(valid):

                                if(newTx.outputAddress != newTx.public):

                                    blockchain.new_transaction(newTx.public, newTx.outputAddress, newTx.outputAmount)

                                    newBlock = blockchain.goNewBlock()

                                    if(newBlock):

                                        blockchain.new_block() # Creates new block if block meets all requirements\\

                                        #verifyBlock(blockchain.last_block_blockchain(), db)

                                    print(colored("[Share Accepted] Share validated", 'green'))
                                else:
                                    print(colored("[Share Rejected] User attempting to send coins to themself.", 'yellow'))

                            #print(block)
                        
                        else:
                            print(colored("[Share Rejected] User balance is too low to make transaction", 'yellow'))
    
    #except Exception as e:
        #print(colored("[FATAL ERROR] Miner error occured. " + str(e) + " Restart miner.", 'red'))
                
def spamManagement():
    global walletTxFreq

    print(colored('[MINER CORE] Started spam protection service','cyan'))
    

    while True:
        time.sleep(86400) # Set seconds to 24 hours
        walletTxFreq = {} # Resets wallet spam threshold periodically


if __name__ == "__main__":


    # Loads node configuration

    loadComplete = loadConfiguration()

    if(NETWORK == "testnet"):
        print(colored("[VALIDATOR CORE][WARNING] Validator node is running in testnet mode. If you want to run in mainnet, change the 'network' option to 'mainnet' in the config.json", "yellow"))

    time.sleep(3)

    if(loadComplete):


        # Creates the /blockchain dir if not exist
        current_directory = os.getcwd()

        final_directory = os.path.join(current_directory, r'Blockchain')
        if not os.path.exists(final_directory):
            print("Creating blockchain directory")
            os.makedirs(final_directory)

    
        print("Starting archival server")

        # Syncs the blockchain

        syncUtil = BlockchainSyncUtil.BlockchainSyncUtil()

        nodesData = syncUtil.getNodes(NETWORK)

        execute = False

        currentTransactions = None

        while True:

            #print(nodesData)

            # IF getNodes is None

            if(nodesData == None):
                execute = False
                print("Error with connecting to network node. Restart miner and try again later.")
                break

            #print("Repeat")

            syncNodeIP, syncNodePort, nodeDataJSON = syncUtil.getRandomNode(MINER_ID, nodesData)


            if(syncNodeIP == True and syncNodePort == True and nodeDataJSON == True): # This is the first online node

                print("Detected as first online node")

                execute = True

                break


            elif(syncNodeIP != None and syncNodePort != None and nodeDataJSON != None): # Is 

                syncComplete, currentTx = syncUtil.chainInitSync(syncNodeIP, syncNodePort) # Blockchain is attempted to be synced

                if(syncComplete): # If blockchain is synced
                    execute = True 
                    currentTransactions = currentTx
                    break
                    
                else: # Sync failed
                    # Remove this node from list
                    nodesData['data'].remove(nodeDataJSON)
                    pass


            else: # Blockchain could not be synced
                #nodesData
                print("An error has occured with syncing the blockchain")

                execute = False

        if(execute):
            # Starts the main threads
            t1 = threading.Thread(target=archiveServer, args=(('0.0.0.0', TCP_PORT), ))

            grok = threading.Thread(target=runGrok)

            # Starts spam protection service
            spamProtection = threading.Thread(target=spamManagement)

            # Starts the threads
            grok.start()
            t1.start()
            spamProtection.start()

        else:
            x = input(">>")

    
    else: # Error has occured
        x = input(">>")

#except Exception as e:
#print("Error with miner: " + str(e))
#x = input(">>")