# Imports

from connections import Connections


try:
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
    import struct

    import BlockchainSyncUtil as BlockchainSyncUtil
    from Logger import Logger

    import os.path
    from os import path

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
    SPAM_MANAGEMENT_SECONDS_LEFT = 86400
    SPAM_MANAGEMENT_SECONDS_LEFT_DOCUMENT = SPAM_MANAGEMENT_SECONDS_LEFT

    walletTxFreq = {}

    txRecv = []

    validatorLogger = Logger()

    sys.setrecursionlimit(1000000)

    def loadConfiguration():

        global NGROK_AUTH_TOKEN
        global MINER_ID
        global NETWORK
        global validatorLogger

        try:
            with open('config.json', 'r') as file:
                data = json.load(file)

                try: # Checks if ngrokAuthToken exists

                    NGROK_AUTH_TOKEN = data['ngrokAuthToken']

                    # Checks if ngrokAuthToken is proper

                    if(isinstance(NGROK_AUTH_TOKEN, str) != True):
                        validatorLogger.logMessage("Error with loading config.json: key ngrokAuthToken is not of type string", 'error')
                        return False

                except Exception as e:
                    validatorLogger.logMessage("Error with loading config.json: key ngrokAuthToken does not exist", 'error')
                    return False


                try: # Checks if minerID exists
                    MINER_ID = data['minerID']

                    
                    if(isinstance(MINER_ID, str) != True): # Checks if minerID is proper
                        validatorLogger.logMessage("Error with loading config.json: key minerID is not of type string", 'error')
                        return False

                except Exception as e:
                    validatorLogger.logMessage("Error with loading config.json: key minerID does not exist", 'error')
                    return False
                

                try: # Checks if network exists
                    NETWORK = data['network']

                    
                    if(isinstance(MINER_ID, str) and (NETWORK == "mainnet" or NETWORK == "testnet")): # Checks if network is proper
                        pass
                    
                    else: 
                        validatorLogger.logMessage("Error with loading config.json: key network is not of type string or is not 'mainnet' or 'testnet'", 'error')
                        return False

                except Exception as e:
                    validatorLogger.logMessage("Error with loading config.json: key network does not exist", 'error')
                    return False


                # If all values successfull load
                validatorLogger.logMessage("[MINER CORE] Loaded Miner Configs from config.json", 'success')
                return True

        
        # Error with file loading
        except Exception as e:
            validatorLogger.logMessage("Error with loading config.json or file does not exist: " + str(e), 'error')
            return False


    def runGrok():

        global db
        global MINER_ID
        global NGROK_IP
        global NGROK_PORT
        global NETWORK

        # 1sbjL6HgcrNZeVi61XPymtYEisD_xaXYnSwRckKbJiUmBfVg   ---  token for mcendercraftnetwork@gmail.com

        try:
            ngrok.set_auth_token(NGROK_AUTH_TOKEN) # token for krishnatechpranav@gmail.com
            tunnel = ngrok.connect(TCP_PORT, "tcp")
            validatorLogger.logMessage("[Internal Server] Running ngrok connection server: " + str(tunnel.public_url), 'regular')

            NGROK_IP, NGROK_PORT = SocketUtil.updateMinerIp(tunnel.public_url, MINER_ID, NETWORK)

            if(NGROK_IP == None and NGROK_PORT == None):
                validatorLogger.logMessage("[Offline] Cannot connect to network node. Your node will not be connected to the rest of the network, restart this node or try again later.", 'error')
                print(colored("[Offline]") + " Cannot connect to network node. Your node will not be connected to the rest of the network, restart this node or try again later.")
                os._exit(0)

        except Exception as er:
            validatorLogger.logMessage(er, 'error')
            os._exit(0)


    def recvObj(socket, blockchainObj, syncUtil):
        global txRecv
        global SPAM_MANAGEMENT_SECONDS_LEFT_DOCUMENT
        global walletTxFreq

        new_sock = None

        try:
            inputs, outputs, errs = select.select([socket], [], [socket], 6)

            if socket in inputs:


                new_sock, addr = socket.accept()

                #print("Accepted a connection request from %s:%s"%(addr[0], addr[1]));
                
                all_data = b''

                #while True:
                packet = new_sock.recv(1048576)

                print(sys.getsizeof(packet))
                    #if not packet: break
                all_data = all_data + packet
                
                returnData = pickle.loads(all_data)


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
                    validatorLogger.logMessage('Blockchain sync requested from miner: ' + str(addr[0]) + ":" + str(addr[1]), 'regular')

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

                    validatorLogger.logMessage('[WALLET REQUEST] Wallet request for balance', 'info-blue')

                    time.sleep(1)

                    publicUser = ''

                    #Blockchain.getUserBalance(publicUser)

                    index = str(returnData).index(":")

                    publicKey = returnData[index - 1:]

                    userCurrentBalance = blockchainObj.getUserBalance(publicKey)

                    #print("user balance: " +str(userCurrentBalance))

                    new_sock.send(str(userCurrentBalance).encode('utf-8'))

                    #print("Sent user the balance data")

                    validatorLogger.logMessage('[WALLET REQUEST ACCEPTED] Wallet request for balance sent to wallet', 'info-blue')



                    #print("send_user_balance_command for public key: " + str(publicKey))
                    return None
                
                elif('sync_spam_management' in str(returnData)): # Get user balance and send to user

                    validatorLogger.logMessage('[VALIDATOR REQUEST] Validator request for sync spam management', 'info')


                    new_sock.send(pickle.dumps({'secondsLeft': SPAM_MANAGEMENT_SECONDS_LEFT_DOCUMENT, 'walletsList': walletTxFreq}))

                    return None

                
                elif('ping' in str(returnData)): # Get user balance and send to user
                    #print('Validator pinged')

                    #block = returnData

                    #BlockchainSyncUtil.verifyBlock()

                    #BlockchainSyncUtil.sendRecievedBlock(block, blockchainObj, new_sock)

                    time.sleep(0.5)

                    managers = Connections().getManagerNodes()

                    #print(colored("[MINER CORE] Sending request for validator reward", "cyan"))

                    for manager in managers:
                        try:
                            SocketUtil.sendObj(manager['ip'], 'pong:' + str(MINER_ID), manager['port'])

                        except:
                            pass

                    #new_sock.send(str('pong').encode('utf-8'))

                    return None
                
                else:
                    return pickle.loads(all_data)
            else:
                return None
        
        except Exception as e:
            validatorLogger.logMessage("[FATAL ERROR] Error recieving object from client: " + str(e), 'error')
            logging.exception('message')
            return None

    def addTxToList(tx):
        global txRecv
        txRecv.append(pickle.dumps(tx))


    def validatorServer(my_addr):

        try:

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
                    newTx = recvObj(server, blockchain, syncUtil)
                    #txPacket = recvObj(server, blockchain, syncUtil)

                    #if(txPacket != None):

                        #newTx = txPacket.getTransaction()

                        #addr, wifNOTUSEFUL = SignaturesECDSA().make_address(txPacket.getPublic().to_string())

                        #if(addr == 'LC1GeXxDPq69sUzG1Z75Ut6Hsxtz4LhNgBeR'): # If public key matches wallet
                            #print("WALLET is good")
                            #if(txPacket.verifySig(newTx)): # IF transaction is fully valid
                                
                                ###################################
                                # Propogates transaction to other nodes
                                ###################################

                    '''           
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
                    '''

                    if(newTx != None):
                        #print(newTx)

                        blockchain.checkCoinsInCirculation()

                        validatorLogger.logMessage("[Share Recieved] Transaction share recieved - Validating...", 'success')

                        util = SocketUtil()

                        if(newTx.getMetaData() == 'validator_reward'): # For validator reward transaction

                            valid = util.verifyTransaction(newTx, newTx.getPublic())

                            if(valid): # Checks if TX is valid

                                addrOwnWallet, wif = SignaturesECDSA().make_address(newTx.getPublic().to_string())

                                if(addrOwnWallet == 'LC1D9x7UovnwqekVXtKg5BsykBybf9ZsHErh'): #Checks if reward TX is from manager node wallet

                                    validatorLogger.logMessage("[Share Accepted] Validator reward transaction is valid", 'success')

                                    if(blockchain.checkCoinsInCirculation() + newTx.getOutputAmount() <= 146692378):

                                        blockchain.new_transaction('validator_reward', newTx.getOutputAddress(), newTx.getOutputAmount())

                                        addTxToList(newTx)

                                        newBlock = blockchain.goNewBlock()

                                        if(newBlock):
                                            
                                            validatorLogger.logMessage("[BLOCKCHAIN] Block complete. Adding block to the blockchain", 'regular')

                                            blockchain.new_block() # Creates new block if block meets all requirements
                                    
                                    else:
                                        validatorLogger.logMessage("[Share Rejected] Coin limit reached", 'info-red')

                                
                                else:
                                    validatorLogger.logMessage("[Share Rejected] Validator reward transaction is fraud (incorrect signed address)", 'info-red')
                            
                            else:
                                validatorLogger.logMessage("[Share Rejected] Validator reward transaction is not valid", 'info-red')


                        else: # For regular trasaction


                            addrSimplified = newTx.getOwnWallet()

                            #addrSimplified = addrSimplified.replace(b'-----BEGIN PUBLIC KEY-----\n', b'')
                            #addrSimplified = addrSimplified.replace(b'\n-----END PUBLIC KEY-----\n', b'')

                            # Handles spam management

                            if (walletTxFreq.get(addrSimplified) != None):
                                walletTxFreq[addrSimplified] = walletTxFreq[addrSimplified] + 1
                            else:
                                walletTxFreq[addrSimplified] = 1

                            
                            if(walletTxFreq.get(addrSimplified) > 200000000000): # If wallet spams
                                validatorLogger.logMessage("[Share Rejected] Wallet address is executing too many transactions", 'warning')

                            else: # If wallet does not spam

                                #print(newTx)
                                valid = util.verifyTransaction(newTx, newTx.getPublic())

                                addrOwnWallet, wif = SignaturesECDSA().make_address(newTx.getPublic().to_string())

                                if(addrOwnWallet == newTx.getOwnWallet()):

                                    if(newTx.getOwnWallet() != "genesis" and newTx.getOwnWallet() != "validator_reward"):

                                        userCurrentBalance = blockchain.getUserBalance(newTx.getOwnWallet())
                                    
                                        #print(userCurrentBalance)

                                        print(newTx.getOwnWallet())
                                        print(userCurrentBalance)

                                        print(newTx.getOutputAmount())

                                        if(userCurrentBalance >= newTx.getOutputAmount()):

                                            if(valid):

                                                if(newTx.getOutputAddress() != newTx.getPublic()):

                                                    blockchain.new_transaction(newTx.getOwnWallet(), newTx.getOutputAddress(), newTx.getOutputAmount())


                                                    # Adds transaction hash to list

                                                    #tx_string = json.dumps(newTx, sort_keys=True).encode()
                                                    #tx_hash = hashlib.sha256(tx_string).hexdigest()

                                                    addTxToList(newTx)

                                                    newBlock = blockchain.goNewBlock()

                                                    if(newBlock):

                                                        validatorLogger.logMessage("[BLOCKCHAIN] Block complete. Adding block to the blockchain", 'regular')

                                                        blockchain.new_block() # Creates new block if block meets all requirements\\


                                                        #verifyBlock(blockchain.last_block_blockchain(), db)
                                                    validatorLogger.logMessage("[Share Accepted] Share validated", 'success')

                                                else:
                                                    validatorLogger.logMessage("[Share Rejected] User attempting to send coins to themself.", 'info-yellow')

                                            #print(block)
                                        
                                        else:

                                            validatorLogger.logMessage("[Share Rejected] User balance is too low to make transaction", 'inof-yellow')
                                    
                                    else:

                                        validatorLogger.logMessage("[Share Rejected] Fraud transaction detected", 'info-yellow')


                                else:
                                    validatorLogger.logMessage("[Share Rejected] Wallet address does not match public key", 'info-yellow')


                except Exception as e:
                    validatorLogger.logMessage("[FATAL ERROR] Error occured with recieving data. " + str(e), 'error')
                    #logging.log('message')

        except Exception as e:
            validatorLogger.logMessage("[FATAL ERROR] Miner error occured. " + str(e) + " Restart node.", 'error')

    def validatorRewardService():
        global txRecv
        global NETWORK
        global MINER_ID
        global NGROK_PORT
        global NGROK_IP
        global wall

        while True:

            time.sleep(20) # Executes every 24 hours

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

                    managers = Connections().getManagerNodes()
                    validatorLogger.logMessage("[MINER CORE] Sending request for validator reward", 'info')

                    for manager in managers:
                        try:
                            SocketUtil.sendObj(manager['ip'], data, manager['port'])

                        except:
                            pass
            
            time.sleep(5)
            #txRecv = [] # Clears transactions list



    def spamManagement():
        global walletTxFreq
        global validatorLogger
        global SPAM_MANAGEMENT_SECONDS_LEFT
        global SPAM_MANAGEMENT_SECONDS_LEFT_DOCUMENT

        validatorLogger.logMessage('[MINER CORE] Started spam protection service', 'info')
        

        while True:

            for i in range(SPAM_MANAGEMENT_SECONDS_LEFT, -1, - 1):
                time.sleep(1)
                SPAM_MANAGEMENT_SECONDS_LEFT_DOCUMENT = SPAM_MANAGEMENT_SECONDS_LEFT_DOCUMENT - 1
                #print(i)

            
            walletTxFreq = {} # Resets wallet spam threshold periodically
            SPAM_MANAGEMENT_SECONDS_LEFT = 86400
            SPAM_MANAGEMENT_SECONDS_LEFT_DOCUMENT = SPAM_MANAGEMENT_SECONDS_LEFT


    if __name__ == "__main__":

        # Checks if miner wallet exists
        if(path.exists('key.pem')):


            # Loads node configuration

            loadComplete = loadConfiguration()

            if(NETWORK == "testnet"):
                validatorLogger.logMessage("[VALIDATOR CORE][WARNING] Validator node is running in testnet mode. If you want to run in mainnet, change the 'network' option to 'mainnet' in the config.json", 'warning')

            time.sleep(3)

            if(loadComplete):

                # Creates the /blockchain dir if not exist
                current_directory = os.getcwd()

                final_directory = os.path.join(current_directory, r'Blockchain')
                if not os.path.exists(final_directory):
                    validatorLogger.logMessage('Creating blockchain directory', 'regular')
                    os.makedirs(final_directory)

                validatorLogger.logMessage('Starting validator node', 'regular')

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
                        validatorLogger.logMessage('Error with connecting to network node. Restart miner and try again later.', 'regular')
                        break

                    #print("Repeat")

                    syncNodeIP, syncNodePort, nodeDataJSON = syncUtil.getRandomNode(MINER_ID, nodesData)


                    if(syncNodeIP == True and syncNodePort == True and nodeDataJSON == True): # This is the first online node
                        
                        validatorLogger.logMessage('[ONLINE] Detected as first online node', 'regular', False)

                        print("[ONLINE " + colored("⦾", 'green') + " ] Detected as first online node")

                        execute = True

                        break


                    elif(syncNodeIP != None and syncNodePort != None and nodeDataJSON != None): # Is 

                        syncComplete, currentTx = syncUtil.chainInitSync(syncNodeIP, syncNodePort) # Blockchain is attempted to be synced

                        if(syncComplete): # If blockchain is synced

                            seconds, txFreqRecv = syncUtil.syncSpamManagementClock(syncNodeIP, syncNodePort)

                            #print(seconds)
                            #print(txFreqRecv)

                            if(seconds != None and txFreqRecv != None):
                                SPAM_MANAGEMENT_SECONDS_LEFT = seconds
                                walletTxFreq = txFreqRecv

                            execute = True 
                            currentTransactions = currentTx


                            break
                            
                        else: # Sync failed
                            # Remove this node from list
                            nodesData['data'].remove(nodeDataJSON)
                            pass


                    else: # Blockchain could not be synced
                        #nodesData
                        validatorLogger.logMessage('An error has occured with syncing the blockchain', 'regular')

                        execute = False

                if(execute):
                    # Starts the main threads
                    t1 = threading.Thread(target=validatorServer, args=(('0.0.0.0', TCP_PORT), ))

                    grok = threading.Thread(target=runGrok)

                    # Starts spam protection service
                    spamProtection = threading.Thread(target=spamManagement)

                    validatorRewardServ = threading.Thread(target=validatorRewardService)

                    # Starts the threads
                    try:
                        grok.start()
                        t1.start()
                        spamProtection.start()
                        validatorRewardServ.start()
                    
                    except Exception as err:
                        validatorLogger.logMessage("Node err has occured: " + str(err), 'regular')

                else:
                    x = input(">>")

            
            else: # Error has occured
                x = input(">>")

        else:
            validatorLogger.logMessage("Miner wallet does not exist. Run 'python GenerateWallet.py' and run the validator node again.", 'error')
            x = input(">>")

except Exception as e:
    print("Error with validator: " + str(e))
    x = input(">>")