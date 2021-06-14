# Imports

#try:
from SignaturesECDSA import SignaturesECDSA
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
import hashlib
import logging
from Transaction import Transaction
import hashlib
import os

import BlockchainSyncUtil as BlockchainSyncUtil

init()
# Global var
TCP_PORT = 6003
BUFFER_SIZE = 65536

CURRENT_BLOCK = None
NGROK_AUTH_TOKEN = None
MINER_ID = None

NGROK_IP = None
NGROK_PORT = None
NETWORK = None

walletTxFreq = {}

txRecv = []

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
    print("[Internal Server] Running ngrok connection server: " + str(tunnel.public_url))

    NGROK_IP, NGROK_PORT = SocketUtil.updateMinerIp(tunnel.public_url, MINER_ID, NETWORK)




def recvObj(socket, blockchainObj, syncUtil):
    global txRecv

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

            '''
            if('validator_reward_transaction' in str(returnData)): # If tx is miner transaction
                print("Validator reward tx")

                rtnDataSTR = str(returnData)
                minerPublic = bytes(rtnDataSTR[rtnDataSTR.find(":") + 1: rtnDataSTR.find("&&&")], 'utf-8').decode('unicode-escape').encode("ISO-8859-1")

                txList = eval(rtnDataSTR[rtnDataSTR.find("&&&")+3:len(rtnDataSTR) - 1])
                
                txValidatedCnt = 0
                txAccuracy = 0.1

                for i in range(len(txRecv)):
                    try:
                        if(txRecv[i] in txList):
                            txValidatedCnt += 1
                    
                    except:
                        pass
                
                #print("VALIDATED: " + str(txValidatedCnt))

                #print("LEN OF TX RECV: " + str(len(txRecv)))

                print(txList)
                print(txRecv)

                try:
                    txAccuracy = txValidatedCnt/len(txRecv) * 100
                
                except Exception as e: #Zero division error
                    print(e)
                    pass

                PAY_VALIDATOR_REWARD = False

                if(len(txList) == 0 and len(txRecv) == 0): # IF both lists are empty (no transactions made)
                    PAY_VALIDATOR_REWARD = True
                
                elif(len(txList) <= 4): # If transactions count is low
                    if(txAccuracy >= 50.0):
                        PAY_VALIDATOR_REWARD = True


                elif(txAccuracy >= 80.0): # Regular transaction count
                    PAY_VALIDATOR_REWARD = True

                #print(txList)
                print(txAccuracy)

                #print(minerPublic)

                if(PAY_VALIDATOR_REWARD == True):
                    Tx = Transaction("validator_reward")
                    Tx.addOutput(minerPublic, 100)
                    #print(minerPublic)
                    Tx.sign(minerPublic, True) 

                    print(colored("[VALIDATOR REWARD] Paying miner reward", "yellow"))

                    return Tx
                
                else:

                    print(colored("[VALIDATOR REWARD] Not paying miner reward as miner proof of work is not sufficient", "yellow"))
                    return None
            '''

            if('blockchain_init_sync' in str(returnData)): # Get user balance and send to user
                print('Blockchain sync requested from miner: ' + str(addr[0]) + ":" + str(addr[1]))

                #block = returnData

                #BlockchainSyncUtil.verifyBlock()

                #BlockchainSyncUtil.sendRecievedBlock(block, blockchainObj, new_sock)

                syncUtil.sendBlockchain(new_sock, blockchainObj)

                return None


            elif('send_transactions_list' in str(returnData)):
                
                dat = pickle.dumps(txRecv)

                new_sock.send(dat)

                #print(txRecv)

                #print("Sending transactions list")

                return None

            elif('send_user_balance_command' in str(returnData)): # Get user balance and send to user

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
        return None

def addTxToList(tx):
    global txRecv
    m = hashlib.sha256()
    m.update(pickle.dumps(tx))
    dig = m.hexdigest()
    txRecv.append(dig)


def validatorServer(my_addr):

    #try:

        global tx_list
        global break_now
        global walletTxFreq
        global txRecv

        blockchain = Blockchain()

        syncUtil = BlockchainSyncUtil.BlockchainSyncUtil()

        my_ip, my_port = my_addr
        # Open server connection
        server = SocketUtil.newServerConnection(my_ip, my_port)

        while True:
            try:
                txPacket = recvObj(server, blockchain, syncUtil)

                if(txPacket != None):

                    newTx = txPacket.getTransaction()

                    addr, wifNOTUSEFUL = SignaturesECDSA().make_address(txPacket.getPublic().to_string())

                    if(addr == 'LC1GeXxDPq69sUzG1Z75Ut6Hsxtz4LhNgBeR'): # If public key matches wallet
                        print("WALLET is good")
                        if(txPacket.verifySig(newTx)): # IF transaction is fully valid
                            
                            ###################################
                            # Propogates transaction to other nodes
                            ###################################


                            while True:
                                nodesRemaining = txPacket.getNodes()
                                if(len(nodesRemaining) == 0):
                                    break
                                
                                else:
                                    try:
                                        util.sendObj(nodesRemaining[0]['ipAddr'], txPacket, int(nodesRemaining[0]['portNumber']))
                                        break

                                    except Exception as e:
                                        txPacket.updateCompletedNode(nodesRemaining[0])
                                        pass
                            
                            print("Finished propogating to other nodes")




                            if(newTx != None):
                                #print(newTx)
                                print(colored("[Share Recieved] Transaction share recieved - Validating...", "green"))

                                util = SocketUtil()

                                if(newTx.metaData == 'validator_reward'): # For validator reward transaction

                                    valid = util.verifyTransaction(newTx, newTx.public)

                                    if(valid): # Checks if TX is valid

                                        addrOwnWallet, wif = SignaturesECDSA().make_address(newTx.public.to_string())

                                        if(addrOwnWallet == 'LC1D9x7UovnwqekVXtKg5BsykBybf9ZsHErh'): #Checks if reward TX is from manager node wallet
                                            
                                            print(colored("[Share Accepted] Validator reward transaction is valid", "green"))

                                            blockchain.new_transaction(newTx.ownWallet, newTx.outputAddress, newTx.outputAmount)

                                            addTxToList(newTx)

                                            newBlock = blockchain.goNewBlock()

                                            if(newBlock):
                                                
                                                print("[BLOCKCHAIN] Block complete. Adding block to the blockchain")
                                                blockchain.new_block() # Creates new block if block meets all requirements
                                        
                                        else:
                                            print(colored("[Share Rejected] Validator reward transaction is fraud (incorrect signed address)", "red"))
                                    
                                    else:
                                        print(colored("[Share Rejected] Validator reward transaction is not valid", "red"))

                                else: # For regular trasaction


                                    addrSimplified = newTx.ownWallet

                                    #addrSimplified = addrSimplified.replace(b'-----BEGIN PUBLIC KEY-----\n', b'')
                                    #addrSimplified = addrSimplified.replace(b'\n-----END PUBLIC KEY-----\n', b'')

                                    # Handles spam management

                                    if (walletTxFreq.get(addrSimplified) != None):
                                        walletTxFreq[addrSimplified] = walletTxFreq[addrSimplified] + 1
                                    else:
                                        walletTxFreq[addrSimplified] = 1

                                    
                                    if(walletTxFreq.get(addrSimplified) > 2000): # If wallet spams
                                        print(colored("[Share Rejected] Wallet address is executing too many transactions", "yellow"))

                                    else: # If wallet does not spam

                                        #print(newTx)
                                        valid = util.verifyTransaction(newTx, newTx.public)

                                        addrOwnWallet, wif = SignaturesECDSA().make_address(newTx.public.to_string())

                                        if(addrOwnWallet == newTx.ownWallet):

                                            userCurrentBalance = blockchain.getUserBalance(newTx.ownWallet)
                                        
                                            #print(userCurrentBalance)

                                            if(userCurrentBalance >= newTx.outputAmount):

                                                if(valid):

                                                    if(newTx.outputAddress != newTx.public):

                                                        blockchain.new_transaction(newTx.ownWallet, newTx.outputAddress, newTx.outputAmount)


                                                        # Adds transaction hash to list

                                                        #tx_string = json.dumps(newTx, sort_keys=True).encode()
                                                        #tx_hash = hashlib.sha256(tx_string).hexdigest()

                                                        addTxToList(newTx)

                                                        newBlock = blockchain.goNewBlock()

                                                        if(newBlock):
                                                            print("[BLOCKCHAIN] Block complete. Adding block to the blockchain")

                                                            blockchain.new_block() # Creates new block if block meets all requirements\\

                                                            #verifyBlock(blockchain.last_block_blockchain(), db)

                                                        print(colored("[Share Accepted] Share validated", 'green'))
                                                    else:
                                                        print(colored("[Share Rejected] User attempting to send coins to themself.", 'yellow'))

                                                #print(block)
                                            
                                            else:
                                                print(colored("[Share Rejected] User balance is too low to make transaction", 'yellow'))
                                        else:
                                            print(colored("[Share Rejected] Wallet address does not match public key", 'yellow'))

            except Exception as e:
                print(colored("[FATAL ERROR] Error occured with recieving data. " + str(e), 'red'))
                logging.log('message')

    #except Exception as e:
        #print(colored("[FATAL ERROR] Miner error occured. " + str(e) + " Restart miner.", 'red'))

def validatorRewardService():
    global txRecv
    global NETWORK
    global MINER_ID
    global NGROK_PORT
    global NGROK_IP
    global wall

    while True:

        time.sleep(10) # Executes every 24 hours

        #print("Paying validator reward")

        #print("TX List: " + str(txRecv))

        nodesData = syncUtil.getNodes(NETWORK)

        if(nodesData != None):
            if(nodesData['status'] == 'success'):
                nodes = nodesData['data']

                #{'ip': '4.tcp.ngrok.io', 'network': 'testnet', 'nodeID': 'default', 'port': '15793'}

                myPrivateSigning, myVerifyingKey = SignaturesECDSA().loadKey()
                walletAddress, wif = SignaturesECDSA().make_address(myVerifyingKey.to_string())
                
                #for node in nodes:

                data = {'walletAddress': walletAddress, 'transactions': txRecv, 'minerID': MINER_ID, 'network': NETWORK, 'ip': NGROK_IP, 'port': NGROK_PORT}

                managers = SocketUtil.getManagerNodes()

                print(colored("[MINER CORE] Sending request for validator reward", "cyan"))

                for manager in managers:
                    try:
                        SocketUtil.sendObj(manager['ip'], data, manager['port'])

                    except:
                        pass
        
        time.sleep(5)
        #txRecv = [] # Clears transactions list



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

    
        print("Starting validator node")

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

                print("[ONLINE " + colored("⦾", 'green') + " ] Detected as first online node")

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
            t1 = threading.Thread(target=validatorServer, args=(('0.0.0.0', TCP_PORT), ))

            grok = threading.Thread(target=runGrok)

            # Starts spam protection service
            spamProtection = threading.Thread(target=spamManagement)

            validatorRewardServ = threading.Thread(target=validatorRewardService)

            # Starts the threads
            grok.start()
            t1.start()
            spamProtection.start()
            #validatorRewardServ.start()

        else:
            x = input(">>")

    
    else: # Error has occured
        x = input(">>")

#except Exception as e:
#print("Error with miner: " + str(e))
#x = input(">>")