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

import BlockchainSyncUtil as BlockchainSyncUtil

init()
# Global var
TCP_PORT = 5005
BUFFER_SIZE = 1024
DOC_ID = ""

CURRENT_BLOCK = None
NGROK_AUTH_TOKEN = None
MINER_ID = None

NGROK_IP = None
NGROK_PORT = None

txValidated = []


sys.setrecursionlimit(1000000)

walletTxFreq = {}


def loadConfiguration():

    global NGROK_AUTH_TOKEN
    global MINER_ID

    try:
        with open('config.json', 'r') as file:
            data = json.load(file)

            NGROK_AUTH_TOKEN = data['ngrokAuthToken']
            MINER_ID = data['minerID']

            print(colored("[MINER CORE] Loaded Miner Configs from config.json", "cyan"))

            return True


    except Exception as e:
        print(colored("Error with loading config.json or file does not exist: " + str(e), "red")) 

        return False


def runGrok():

    global db
    global MINER_ID
    global DOC_ID
    global NGROK_IP
    global NGROK_PORT

    # 1sbjL6HgcrNZeVi61XPymtYEisD_xaXYnSwRckKbJiUmBfVg   ---  token for mcendercraftnetwork@gmail.com

    ngrok.set_auth_token(NGROK_AUTH_TOKEN) # token for krishnatechpranav@gmail.com
    tunnel = ngrok.connect(TCP_PORT, "tcp")
    print("Running ngrok connection server: " + str(tunnel.public_url))

    DOC_ID, NGROK_IP, NGROK_PORT = SocketUtil.updateMinerIp(db, tunnel.public_url, MINER_ID)

        

def recvObj(socket, blockchainObj):

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

            if(isinstance(returnData, Blockchain)):
                print('block recieved to verify')

                block = returnData

                #BlockchainSyncUtil.verifyBlock()

                BlockchainSyncUtil.sendRecievedBlock(block, blockchainObj, new_sock)
                



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


def minerServer(my_addr, blockchain):

    try:

        global tx_list
        global break_now
        global walletTxFreq


        minerPrivate, minerPublic = Signatures().load_key('privateKey.pem')

        my_ip, my_port = my_addr
        # Open server connection
        server = SocketUtil.newServerConnection(my_ip, my_port)


        while True:
            newTx = recvObj(server, blockchain )

            if(newTx != None):
                print(colored("[Share Recieved] Transaction share recieved - Validating...", "green"))

                util = SocketUtil()

                #print(newTx)


                if(newTx.public == 'mining_reward'): #  Checks if block is miner reward

                    print("miner reward transaction")

                    blockchain.new_transaction(newTx.public, newTx.outputAddress, newTx.outputAmount)

                    newBlock = blockchain.goNewBlock()

                    if(newBlock):

                        #blockchain.payMinerReward(minerPublic, ) # Pays mining reward

                        blockchain.new_block() #  Creates new block if block meets all requirements
                    
                    print(colored("[Share Accepted] Share validated", 'green'))

                else:  #  For regular transactions
                    
                    # Registers transactions frequency to check for spam

                    addrSimplified = newTx.public

                    addrSimplified = addrSimplified.replace(b'-----BEGIN PUBLIC KEY-----\n', b'')
                    addrSimplified = addrSimplified.replace(b'\n-----END PUBLIC KEY-----\n', b'')

                    addrSimplified = str(addrSimplified, 'utf-8')

                    if (walletTxFreq.get(addrSimplified) != None):
                        walletTxFreq[addrSimplified] = walletTxFreq[addrSimplified] + 1
                    else:
                        walletTxFreq[addrSimplified] = 1

                    
                    if(walletTxFreq.get(addrSimplified) > 100): # If wallet spams
                        print(colored("[Share Rejected] Wallet address is executing too many transactions", "yellow"))

                    else: # If wallet does not spam


                        valid = util.verifyTransaction(newTx, newTx.public)

                        userCurrentBalance = blockchain.getUserBalance(newTx.public)


                        if(userCurrentBalance >= newTx.outputAmount):

                            if(valid):

                                if(newTx.outputAddress != newTx.public):

                                    blockchain.new_transaction(newTx.public, newTx.outputAddress, newTx.outputAmount)

                                    txValidated.append(newTx)

                                    newBlock = blockchain.goNewBlock()

                                    if(newBlock):

                                        #blockchain.payMinerReward(minerPublic) # Pays mining reward

                                        blockchain.new_block() # Creates new block if block meets all requirements

        

                                    print(colored("[Share Accepted] Share validated", 'green'))
                                else:
                                    print(colored("[Share Rejected] User attempting to send coins to themself.", 'yellow'))

                            #print(block)
                        
                        else:
                            print(colored("[Share Rejected] User balance is too low to make transaction", 'yellow'))
    
    except Exception as e:
        print(colored("[FATAL ERROR] Miner error occured. " + str(e) + " Restart miner.", 'red'))
                
def spamManagement():
    global walletTxFreq

    print(colored('[MINER CORE] Started spam protection service','cyan'))
    

    while True:
        time.sleep(86400) # Set seconds to 24 hours
        walletTxFreq = {} # Resets wallet spam threshold periodically
        





if __name__ == "__main__":

    loadComplete = loadConfiguration()

    if(loadComplete):

        #os.mkdir("/blockchain") # Creates Blockchain Folder
    
        print("Starting miner")
        

        syncUtil = BlockchainSyncUtil.BlockchainSyncUtil()

        syncComplete, currentTransactions = syncUtil.chainInitSync('localhost', 6003)
        

        if(syncComplete):

            blockchain = Blockchain()

            blockchain.current_transactions = currentTransactions

            t1 = threading.Thread(target=minerServer, args=(('0.0.0.0', TCP_PORT), blockchain))

            grok = threading.Thread(target=runGrok)

            spamProtection = threading.Thread(target=spamManagement)

            grok.start()
            t1.start()
            spamProtection.start()

        
        else:
            z = input("Failed to sync blockchain (press any key to quit) >>")

    
    else:
        x = input(">>")

#except Exception as e:
#print("Error with miner: " + str(e))
#x = input(">>")