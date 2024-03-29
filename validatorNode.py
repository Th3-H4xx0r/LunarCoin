'''

888      888     888 888b    888        d8888 8888888b.       .d8888b.   .d88888b.  8888888 888b    888 
888      888     888 8888b   888       d88888 888   Y88b     d88P  Y88b d88P" "Y88b   888   8888b   888 
888      888     888 88888b  888      d88P888 888    888     888    888 888     888   888   88888b  888 
888      888     888 888Y88b 888     d88P 888 888   d88P     888        888     888   888   888Y88b 888 
888      888     888 888 Y88b888    d88P  888 8888888P"      888        888     888   888   888 Y88b888 
888      888     888 888  Y88888   d88P   888 888 T88b       888    888 888     888   888   888  Y88888 
888      Y88b. .d88P 888   Y8888  d8888888888 888  T88b      Y88b  d88P Y88b. .d88P   888   888   Y8888 
88888888  "Y88888P"  888    Y888 d88P     888 888   T88b      "Y8888P"   "Y88888P"  8888888 888    Y888 
                                                                                                                                                                                                                                                        
 __   __         _   _      _          _                   _  _            _       
 \ \ / /  __ _  | | (_)  __| |  __ _  | |_   ___   _ _    | \| |  ___   __| |  ___ 
  \ V /  / _` | | | | | / _` | / _` | |  _| / _ \ | '_|   | .` | / _ \ / _` | / -_)
   \_/   \__,_| |_| |_| \__,_| \__,_|  \__| \___/ |_|     |_|\_| \___/ \__,_| \___| 

 Version: 0.9.0-beta

                                                                                   
Official Website: https://lunarcoin.network

// Copyright 2021 Lunar Coin Developers
// This file is part of the lunarcoin-validator-node library.
//
// The lunarcoin-validator-node library is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// The lunarcoin-validator-node library is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU Lesser General Public License for more details.
//
// You should have received a copy of the GNU Lesser General Public License
// along with the lunarcoin-validator-node library. If not, see <http://www.gnu.org/licenses/>.
'''

# Imports
from asyncio.tasks import FIRST_COMPLETED
from hashlib import new
from logging import BASIC_FORMAT
from re import A
from connections import Connections

try:
    import traceback
    import sys
    from SignaturesECDSA import SignaturesECDSA
    import socket
    import pickle
    import select
    import threading
    from SocketUtil import SocketUtil
    from Signatures import Signatures
    #from Blockchain import Blockchain
    from BlockchainMongo import BlockchainMongo
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
    import asyncio
    import requests
    from hashlib import sha256
    from TransactionPacket import TransactionPacket
    import ecdsa
    import codecs
    import BlockchainSyncUtil as BlockchainSyncUtil
    from Logger import Logger
    import os.path
    from os import path
    import random
    import ntplib
    from time import ctime
    from time import strftime
    from time import gmtime

    ###########################
    # Initilizations
    ###########################
    init()

    ###########################
    # Global Variables
    ###########################
    TCP_PORT = 6003
    BUFFER_SIZE = 65536
    CURRENT_BLOCK = None
    NGROK_AUTH_TOKEN = None
    MINER_ID = None
    NODE_IP = None
    NODE_PORT = None
    NETWORK = None
    BLOCKCHAIN_OBJECT = None
    SPAM_MANAGEMENT_SECONDS_LEFT = 86400
    SPAM_MANAGEMENT_SECONDS_LEFT_DOCUMENT = SPAM_MANAGEMENT_SECONDS_LEFT
    VALIDATOR_PEERS = []
    BLOCKCHAIN_SYNC_COMPLETE = False
    NODE_VERSION = '' # TODO: Add node version to be sent on IHS    
    CONNECTION_MODE = 'tcp'
    VALIDATOR_PRIVATE, VALIDATOR_PUBLIC_KEY = None, None
    VALIDATOR_WALLET_ADDRESS = None
    INITIAL_TWO_BLOCK_PASSED = False
    NODE_UPTIME_START = time.time()
    BLOCK_TIME_PASS_COUNTER = 0
    c = ntplib.NTPClient()
    response = c.request('us.pool.ntp.org', version=3)
    INTERNAL_NODE_CLOCK = response.tx_time
    INTERNAL_NODE_CLOCK += 1
    TIME_THRESHOLD_REACHED = False
    walletTxFreq = {}
    txRecv = []
    validatorLogger = Logger()
    sys.setrecursionlimit(1000000000)

    def internalClockService():
        global INTERNAL_NODE_CLOCK
        while True:
            INTERNAL_NODE_CLOCK += 1
            time.sleep(1)

    def saveBlockService():
        '''
        @@@ Implementation
         - Saves block every 5 minutes
         - New nodes on the network will wait 2 save cycles (600sec) before they save their first block
          -- To allow buffer time so they will be caught up with the network
         - New block is then saved if it meets the transaction count threshold for the current block height
        '''
        
        global TIME_THRESHOLD_REACHED
        global INTERNAL_NODE_CLOCK
        global INITIAL_TWO_BLOCK_PASSED
        global BLOCK_TIME_PASS_COUNTER
        global BLOCKCHAIN_OBJECT
        global VALIDATOR_PEERS
        global NODE_UPTIME_START
        TEMP = time.time()
        while True:
            #print(ctime(start) + str(" : ") + ctime(time.time()))
            seconds = 10 # Saves block every 5 minutes
            diff = INTERNAL_NODE_CLOCK % seconds
            if(str(diff)[0] == '0' and TIME_THRESHOLD_REACHED == False):
                print("----------------")
                print(f"its been {seconds} sec")
                print("ACTUAL: " + str(time.time()-TEMP))
                print("Right Now: " + str(ctime(time.time())))
                print("Total Node Uptime: " + str(strftime("%H:%M:%S", gmtime(time.time() - NODE_UPTIME_START))) + "sec")
                TEMP = time.time()
                BLOCK_TIME_PASS_COUNTER+=1
                if(BLOCK_TIME_PASS_COUNTER > 2):
                    INITIAL_TWO_BLOCK_PASSED = True
                TIME_THRESHOLD_REACHED = True
                # Saves the block
                if(INITIAL_TWO_BLOCK_PASSED):
                    newBlock = BLOCKCHAIN_OBJECT.goNewBlock()
                    if(newBlock):
                        validatorLogger.logMessage("[BLOCKCHAIN] Block complete. Adding block to the blockchain", 'regular')
                        BLOCKCHAIN_OBJECT.new_block(VALIDATOR_PEERS) # Creates new block if block meets all requirements
                    else:
                        print("Not adding block...")
            if(str(diff)[0] != '0' and TIME_THRESHOLD_REACHED == True):
                TIME_THRESHOLD_REACHED = False
            time.sleep(0.1)

    def loadConfiguration():

        global NGROK_AUTH_TOKEN
        global MINER_ID
        global NETWORK
        global validatorLogger
        global CONNECTION_MODE
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
                    validatorLogger.logMessage("Error with loading config.json: key network does not exist: " + str(e), 'error')
                    return False
                try: # Checks if connection mode
                    CONNECTION_MODE = data['connection_mode']
                    if(isinstance(CONNECTION_MODE, str) and (CONNECTION_MODE == "tcp" or CONNECTION_MODE == "ngrok")): # Checks if network is proper
                        pass
                    else: 
                        validatorLogger.logMessage("Error with loading config.json: key connection_mode is not of type string or is not 'tcp' or 'ngrok'", 'error')
                        return False
                except Exception as e:
                    validatorLogger.logMessage("Error with loading config.json: key connection_mode does not exist: " + str(e), 'error')
                    return False
                # If all values successfull load
                validatorLogger.logMessage("[VALIDATOR CORE] Loaded validator Configs from config.json", 'success')
                return True
        # Error with file loading
        except Exception as e:
            validatorLogger.logMessage("Error with loading config.json or file does not exist: " + str(e), 'error')
            return False


    def runGrok():

        global db
        global MINER_ID
        global NODE_IP
        global NODE_PORT
        global NETWORK
        global CONNECTION_MODE
        global TCP_PORT
        global VALIDATOR_PUBLIC_KEY
        global VALIDATOR_WALLET_ADDRESS
        global VALIDATOR_PRIVATE
        # 1sbjL6HgcrNZeVi61XPymtYEisD_xaXYnSwRckKbJiUmBfVg   ---  token for mcendercraftnetwork@gmail.com

        if(CONNECTION_MODE == 'ngrok'):
            try:
                ngrok.set_auth_token(NGROK_AUTH_TOKEN) # token for krishnatechpranav@gmail.com
                tunnel = ngrok.connect(TCP_PORT, "tcp")
                validatorLogger.logMessage("[Internal Server] Running ngrok connection server: " + str(tunnel.public_url), 'regular')
                NODE_IP, NODE_PORT = SocketUtil.updateMinerIp(tunnel.public_url, MINER_ID, NETWORK, VALIDATOR_PUBLIC_KEY.to_string().hex(), VALIDATOR_WALLET_ADDRESS, VALIDATOR_PRIVATE)
                if(NODE_IP == None and NODE_PORT == None):
                    validatorLogger.logMessage("[Offline] Cannot connect to network node. Your node will not be connected to the rest of the network, restart this node or try again later. Exiting...", 'error')
                    time.sleep(3)
                    os._exit(0)
            except Exception as er:
                validatorLogger.logMessage(er, 'error')
                time.sleep(3)
                os._exit(0)

        elif(CONNECTION_MODE == 'tcp'):
            NODE_IP = requests.get('https://api.ipify.org').content.decode('utf8')
            NODE_PORT = TCP_PORT
            success = SocketUtil.updateMinerIpTCP_MODE(NODE_IP, TCP_PORT, MINER_ID, NETWORK, VALIDATOR_PUBLIC_KEY.to_string().hex(), VALIDATOR_WALLET_ADDRESS, VALIDATOR_PRIVATE)
            if(success):
                validatorLogger.logMessage("[NODE CONNECTION] Started connection for node with address " + str(NODE_IP) + ":" + str(TCP_PORT) + ". IMPORTANT: Configure your router to port-forward this port and point to this machine.", "info-yellow")
            else:
                print("Error with establishing a connection with the network node. Exiting...")
                time.sleep(3)
                os._exit(0)
        else:
            validatorLogger.logMessage("[OFFLINE] Connection mode is not defined or valid. Exiting...", "error")
            time.sleep(3)
            os._exit(0)

    def recvObj(socket, blockchainObj, syncUtil):
        global txRecv
        global SPAM_MANAGEMENT_SECONDS_LEFT_DOCUMENT
        global walletTxFreq
        new_sock = None
        try:
            #inputs, outputs, errs = select.select([socket], [], [socket], 6)
            #if socket in inputs:
            new_sock, addr = socket.accept()
            #print("Accepted a connection request from %s:%s"%(addr[0], addr[1]));
            all_data = b''
            #while True:
            #packet = new_sock.recv(10485760)
            #print(sys.getsizeof(packet))
                #if not packet: break
            #all_data = all_data + packet
            timeout = 0.1
            #make socket non blocking
            new_sock.setblocking(0)
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
                    data = new_sock.recv(65536)
                    if data:
                        total_data.append(data)
                        #print(sys.getsizeof(data))
                        #change the beginning time for measurement
                        begin=time.time()
                    else:
                        #sleep for sometime to indicate a gap
                        time.sleep(0.1)
                except:
                    pass
                #join all parts to make final string
                all_data = b''.join(total_data)
            #print(sys.getsizeof(all_data))
            #print(all_data)
            if(all_data != b''):
                #####################################
                # Mobile Transaction Handler
                #####################################
                if('mobile_transaction' in str(all_data)):
                    validatorLogger.logMessage('[Share Recieved] Mobile transaction recieved', 'regular')
                    useData = all_data.decode("utf-8") 
                    index = useData.index(":/:")
                    indexEOS = useData.index("EOS")
                    finalData = useData[index + 3:indexEOS]
                    #finalData = "'" + finalData + "'"
                    #print("FINAL DATA FILTERED")
                    jsonParsed = json.loads(finalData)
                    tx_public = ecdsa.VerifyingKey.from_string(bytes.fromhex(jsonParsed['public_key']), curve=ecdsa.SECP256k1, hashfunc=sha256)
                    tx_timestamp = jsonParsed['timestamp']
                    tx_outputAddr = jsonParsed['recipient']
                    tx_amount = jsonParsed['output']
                    tx_signature = jsonParsed['signature']
                    tx_id = jsonParsed['transactionID']
                    metadata = jsonParsed['metadata']
                    tx_wallet = SignaturesECDSA().make_address(tx_public.to_string())
                    if(metadata == 'none'):metadata == 'mobile'

                    if(tx_outputAddr != tx_wallet):
                        mobileTx = Transaction(tx_public, tx_wallet, tx_timestamp, tx_outputAddr, tx_amount, tx_signature, tx_id, jsonParsed['public_key'], metadata)
                        txPacket = TransactionPacket(mobileTx)
                        return txPacket
                    else:
                        validatorLogger.logMessage('[Share Rejected] User is sending coins to themself', 'error')
                        return None
                    #(self, public, timestamp, outputAddr, amount, signature, txID, wallet):
                    #{"recipient":"LC1234","output":10.0,"public_key":"045feff91e0171e2fa0c96863e0b4054747e10e295854b91a5af274c0d2bde908f4f3f9f5a74f6b232b42c1ac3f9d4cb628420fb518bddbe0a7cb8b8a869cd8644","transactionID":"0xSiGc-Fy6RKbmKcsL-_b-00l_rB4PFv0MtaE-2cdIQr38a4ms6oWLeAmqq_uZnWKU","signature":"3090594baad2e5dd00390eb9b184fbdfb453ca6bdef90c9183274196e7acff53d08803f85d3a881e9801d8a265411f5fa234543feec9a89627ccb05591283720"}
                elif('makeAddr' in str(all_data)):
                    validatorLogger.logMessage('[Address Request] Make address request received', 'regular')
                    useData = all_data.decode("utf-8") 
                    index = useData.index(":/:")
                    indexEOS = useData.index("EOS")
                    finalData = useData[index + 3:indexEOS]
                    tx_public = ecdsa.VerifyingKey.from_string(bytes.fromhex(finalData), curve=ecdsa.SECP256k1, hashfunc=sha256)
                    addr = SignaturesECDSA().make_address(tx_public.to_string())
                    new_sock.send(bytes(addr[0], 'utf-8'))
                
                elif('sendAllInvoices' in str(all_data)):
                    validatorLogger.logMessage('[Invoice Request] Mobile invoices request received', 'regular')
                    useData = all_data.decode("utf-8") 
                    index = useData.index(":/:")
                    indexEOS = useData.index("EOS")
                    walletAddr = useData[index + 3:indexEOS]
                    invoices = blockchainObj.get_invoices(walletAddr.encode('utf-8'))

                    for invoice in invoices:
                        del invoice['_id']
                        
                    new_sock.send(str(invoices).encode('utf-8'))

                elif('send_user_balance_command_mobile' in str(all_data)):

                    try:
                        validatorLogger.logMessage('[WALLET REQUEST] Wallet request for balance MOBILE', 'info-blue')
                        useData = all_data.decode("utf-8") 
                        index = useData.index(":")
                        publicKey = useData[index + 1:]
                        userCurrentBalance = blockchainObj.getUserBalance(publicKey, None, None, True, False)
                        returnVar = str(userCurrentBalance[0]) + "://:" + str({"transactions": userCurrentBalance[2]})
                        new_sock.sendall(returnVar.encode('utf-8'))
                    except Exception as e:
                        pass
                
                elif('generate_invoice' in str(all_data)): # Get user balance and send to user
                    validatorLogger.logMessage('[INVOICE CREATE REQUEST] Request to generate invoice - mobile', 'info-blue')
                    all_data = all_data.decode("utf-8") 
                    index = str(all_data).index(":/:")
                    indexEOS = str(all_data).index("EOS")
                    invoiceDetails = json.loads(str(all_data[index + 3:indexEOS]))
                    blockchainObj.create_invoice(invoiceDetails['invoiceID'], invoiceDetails['amount'], invoiceDetails['fromAddr'], invoiceDetails['toAddr'], invoiceDetails['expDate'], invoiceDetails['signature'], invoiceDetails['publicHex'], True)
                    #invoiceID, amount, fromAddr, toAddr, expDate, signature, publicKey
                    return None

                else:
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
                        syncUtil.sendBlockchain_HEADER(new_sock, blockchainObj)
                        return None
                    
                    elif('block_sync' in str(returnData)):
                        index = str(returnData).index(":")
                        index_dash = str(returnData).index("-")
                        height = returnData[index - 1:index_dash - 2].decode("utf-8") 
                        height_end = returnData[index_dash - 1:].decode("utf-8") 
                        validatorLogger.logMessage('Block sync with height: ' + str(height) +  ' to height ' + str(height_end) + ' requested from validator: ' + str(addr[0]) + ":" + str(addr[1]), 'regular')
                        syncUtil.sendBlockchain_BLOCK(new_sock, blockchainObj, height, height_end)
                        return None
                    
                    elif('blockchain_hash_header_sync' in str(returnData)):
                        index = str(returnData).index(":")
                        index_dash = str(returnData).index("-")
                        height = returnData[index - 1:index_dash - 2].decode("utf-8") 
                        height_end = returnData[index_dash - 1:].decode("utf-8") 
                        validatorLogger.logMessage('Block sync hash headers with height: ' + str(height) +  ' to height ' + str(height_end) + ' requested from validator: ' + str(addr[0]) + ":" + str(addr[1]), 'regular')
                        syncUtil.sendBlockchain_BLOCK_HASH_HEADERS(new_sock, blockchainObj, height, height_end)
                        return None

                    elif('send_transactions_list' in str(returnData)):
                        dat = pickle.dumps(txRecv)
                        new_sock.send(dat)
                        return None

                    elif('send_user_balance_command' in str(returnData)): # Get user balance and send to user
                        validatorLogger.logMessage('[WALLET REQUEST] Wallet request for balance', 'info-blue')
                        #time.sleep(1)
                        publicUser = ''
                        #Blockchain.getUserBalance(publicUser)
                        index = str(returnData).index(":")
                        publicKey = returnData[index - 1:]
                        userCurrentBalance = blockchainObj.getUserBalance(publicKey, None, None, False, False)
                        new_sock.sendall(str(userCurrentBalance[0]).encode('utf-8'))
                        validatorLogger.logMessage('[WALLET REQUEST ACCEPTED] Wallet request for balance sent to wallet', 'info-blue')
                        return None
                    
                    elif('generate_invoice' in str(returnData)): # Get user balance and send to user
                        validatorLogger.logMessage('[INVOICE REQUEST] Request to generate invoice', 'info-blue')
                        index = str(returnData).index(":")
                        invoiceDetails = pickle.loads(codecs.decode(str(returnData[index + 1:]).encode(), "base64")) #pickle.loads(bytes(str(returnData[index + 1:]), 'utf-8'))
                        blockchainObj.create_invoice(invoiceDetails['invoiceID'], invoiceDetails['amount'], invoiceDetails['fromAddr'], invoiceDetails['toAddr'], invoiceDetails['expDate'], invoiceDetails['signature'], invoiceDetails['publicHex'])
                        #invoiceID, amount, fromAddr, toAddr, expDate, signature, publicKey
                        return None

                    elif('get_invoices' in str(returnData)): # Get user balance and send to user
                        validatorLogger.logMessage('[INVOICE REQUEST] Request to get invoices', 'info-blue')
                        index = str(returnData).index(":")
                        walletAddr =  returnData[index - 1:]
                        invoices = blockchainObj.get_invoices(walletAddr)
                        new_sock.sendall(pickle.dumps(invoices))
                        #invoiceID, amount, fromAddr, toAddr, expDate, signature, publicKey
                        return None
                    
                    elif('get__invoices_pending_incoming' in str(returnData)): # Get user balance and send to user
                        validatorLogger.logMessage('[INVOICE REQUEST] Request to get pending incoming invoices', 'info-blue')
                        index = str(returnData).index(":")
                        walletAddr =  returnData[index - 1:]
                        invoices = blockchainObj.get_invoices(walletAddr, False)
                        new_sock.sendall(pickle.dumps(invoices))
                        #invoiceID, amount, fromAddr, toAddr, expDate, signature, publicKey
                        return None
                    
                    elif('invoice_pool_init_sync' in str(returnData)): # Get user balance and send to user
                        validatorLogger.logMessage('[INVOICE REQUEST] Request to get pending incoming invoices', 'info-blue')
                        index = str(returnData).index("://:")
                        lastIDInfo =  pickle.loads(returnData[index+4:])
                        print("LAST ID: " + str(lastIDInfo))
                        sent = syncUtil.sendInvoicePool(new_sock, lastIDInfo['lastID'])
                        return None

                    elif('sync_spam_management' in str(returnData)): # Get user balance and send to user
                        validatorLogger.logMessage('[VALIDATOR REQUEST] Validator request for sync spam management', 'info')
                        new_sock.send(pickle.dumps({'secondsLeft': SPAM_MANAGEMENT_SECONDS_LEFT_DOCUMENT, 'walletsList': walletTxFreq}))
                        return None

                        # TODO: For block confirmation
                        '''
                                    elif('block_confirmation' in str(returnData)):
                            # Confirms block

                            validatorLogger.logMessage('[BLOCK CONFIRMATION] Block confirmation requested', 'info')

                            index = str(returnData).index(":")

                            blockReq = pickle.loads(returnData[index + 1:])

                            print(blockReq)
                            
                        '''
                    elif('ping' in str(returnData)): # Get user balance and send to user
                        print('Validator pinged')
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
            #else:
                #return None
                new_sock.close()
        
        except Exception as e:
            validatorLogger.logMessage("[FATAL ERROR] Error recieving object from client: " + str(e), 'error')
            print(traceback.format_exc())
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
            global NODE_PORT
            global NODE_IP
            global VALIDATOR_PEERS
            global BLOCKCHAIN_OBJECT
            BLOCKCHAIN_OBJECT = BlockchainMongo()
            BLOCKCHAIN_OBJECT.initializeBlockchain()
            syncUtil = BlockchainSyncUtil.BlockchainSyncUtil()
            my_ip, my_port = my_addr
            # Open server connection
            server = SocketUtil.newServerConnection(my_ip, my_port)
            while True:
                try:
                    newTx = recvObj(server, BLOCKCHAIN_OBJECT, syncUtil)
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
                        #blockchain.checkCoinsInCirculation()
                        validatorLogger.logMessage("[Share Recieved] Transaction share recieved - Validating...", 'success')
                        ########################################################################################
                        # Propogates transaction to other nodes (P2PP) - Peer to Peer Propgation Protocol
                        ########################################################################################
                        duplicateTransaction = False
                        nodesToSendToTemp = VALIDATOR_PEERS
                        # Checks if transaction packet is already validated by this node
                        peers_recieved = newTx.getNodes()
                        for node in peers_recieved:
                            if(node == {'ip': NODE_IP, 'port': NODE_PORT}):
                                duplicateTransaction = True

                        if(duplicateTransaction == False): #TODO: This is redundant look into
                            # Adds current node to the recieved list on transaction packet
                            newTx.updateCompletedNode({'ip': NODE_IP, 'port': NODE_PORT})
                            #{'ip': '4.tcp.ngrok.io', 'port': 15107, 'status': 'offline'}
                            nodesToSendTo = []
                            #print(nodesToSendTo)
                            # Filters out offline nodes from peers list
                            for node in nodesToSendToTemp:
                                #print("Filtering nodes to send to: " + str(node))
                                try:
                                    if(node['status'] == 'online'):
                                        nodesToSendTo.append(node)
                                
                                except Exception as e:
                                    print("Error with getting nodes to propagate to: " + str(e))

                            # Removes peers that have already recieved the transaction
                            peers_recieved = newTx.getNodes()
                            for node_recv in peers_recieved:
                                for node_peer in nodesToSendTo:
                                    if(node_peer['ip'] == node_recv['ip'] and node_peer['port'] == node_recv['port']):
                                        # Removes the peer from the propagation list
                                        try:
                                            nodesToSendTo.remove(node)
                                        except Exception as e:
                                            pass

                            # TODO: Issue, transaction can be manipulated and sent many times
                            validatorLogger.logMessage("[P2PP] Propogating transaction to peers", 'info')
                            # TODO: Transaction is not checked for same id
                            # Generates two random nodes to propogate to
                            if(len(nodesToSendTo) > 2):
                                print("more than 2 nodes online, generating random number to send to")
                                n1 = random.randint(0, len(nodesToSendTo) - 1)
                                n2 = random.randint(0, len(nodesToSendTo) - 1)
                                if(n2 == n1):
                                    while True:
                                        n2 = random.randint(0, len(nodesToSendTo) - 1)

                                        if(n2 != n1):
                                            break
                                nodesToSendTo = [nodesToSendTo[n1], nodesToSendTo[n2]]
                        
                            # print("NODES TO SEND TO: " + str(nodesToSendTo))
                            #print(VALIDATOR_PEERS)
                            #print(newTx)
                            print("NODES TO SEND TO: " + str(nodesToSendTo))
                            for node in nodesToSendTo:
                                try:
                                    Connections().sendObj(node['ip'], newTx, node['port'])
                                    print("Propagated transaction to node: " + str(node['ip']) + ":" + str(node['port']))
                                
                                except Exception as e:
                                    validatorLogger.logMessage("[Propagation Error] Error propagating transaction to node" + str(node['ip']) + ":" + str(node['port']) + " - " + str(e), 'error')
                                    
                            newTx = newTx.getTransaction()
                            util = SocketUtil()
                            if(newTx.getMetaData() == 'validator_reward'): # For validator reward transaction
                                valid = util.verifyTransaction(newTx, newTx.getPublic())
                                if(valid): # Checks if TX is valid
                                    addrOwnWallet, wif = SignaturesECDSA().make_address(newTx.getPublic().to_string())
                                    if(addrOwnWallet == 'LC1D9x7UovnwqekVXtKg5BsykBybf9ZsHErh'): #Checks if reward TX is from manager node wallet
                                        validatorLogger.logMessage("[Share Accepted] Validator reward transaction is valid", 'success')
                                        #if(blockchain.checkCoinsInCirculation() + newTx.getOutputAmount() <= 146692378): # TODO: FIX THIS
                                        transactionSuccess = BLOCKCHAIN_OBJECT.new_transaction('validator_reward', newTx.getOutputAddress(), newTx.getOutputAmount(), newTx.getTransactionID(), newTx.getTimestamp(), newTx.getHash(), str(newTx.getMetaData()))
                                        if(transactionSuccess):
                                            addTxToList(newTx)
                                            '''
                                            newBlock = BLOCKCHAIN_OBJECT.goNewBlock()

                                            if(newBlock):
                                                
                                                validatorLogger.logMessage("[BLOCKCHAIN] Block complete. Adding block to the blockchain", 'regular')

                                                BLOCKCHAIN_OBJECT.new_block() # Creates new block if block meets all requirements
                                            
                                            #else:
                                                #validatorLogger.logMessage("[Share Rejected] Coin limit reached", 'info-red')
                                            '''
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
                                    madeWalletAddr, wif = SignaturesECDSA().make_address(newTx.getPublic().to_string())
                                    getOwnWalletFunc = newTx.getOwnWallet()
                                    if(newTx.getTxType() == 'mobile'): #TODO: giving tuple for some reason FIX
                                        getOwnWalletFunc = getOwnWalletFunc[0]
                                    
                                    #print("//////////////////////")
                                    #print(madeWalletAddr)
                                    #print(getOwnWalletFunc)
                                    #print("//////////////////////")

                                
                                    if(madeWalletAddr == getOwnWalletFunc):
                                        if(getOwnWalletFunc != "genesis" and getOwnWalletFunc != "validator_reward"):
                                            userCurrentBalance, duplicateTx = BLOCKCHAIN_OBJECT.getUserBalance(getOwnWalletFunc, None, newTx.getTransactionID(), False, False)
                                            if(duplicateTx == False):
                                                if(userCurrentBalance >= newTx.getOutputAmount()):
                                                    if(valid):
                                                        if(newTx.getOutputAddress() != newTx.getPublic()):
                                                            # Transaction is fully processed and is good to go
                                                            #sender, recipient, amount, transactionID, timestamp, hashVal
                                                            execute = True
                                                            if(newTx.getMetaData() != None):   
                                                                if('invoice_send_to' in newTx.getMetaData()):
                                                                    metaData = newTx.getMetaData()
                                                                    invoiceIdGet = newTx.getMetaData()
                                                                    colonIndex = str(metaData).find(":")
                                                                    secondElementIndex = str(metaData).find("://:")
                                                                    invoiceIdGet = metaData[colonIndex + 1: secondElementIndex]
                                                                    invoiceFromAddr = metaData[secondElementIndex+4:]
                                                                    if(invoiceFromAddr == newTx.getOutputAddress()):
                                                                        removeInvResult = BLOCKCHAIN_OBJECT.remove_invoice_from_pool(invoiceIdGet, newTx.getOutputAddress(), newTx.getOwnWallet())
                                                                    else:
                                                                        validatorLogger.logMessage("[Share Rejected] Invoice signature or metadata is corrupt", 'info-yellow')
                                                                        execute = False
                                                                #blockchain.remove_invoice_from_pool(newTx.getOwnWallet(), getOwnWalletFunc)
                                                            # Adds transaction hash to list
                                                            #tx_string = json.dumps(newTx, sort_keys=True).encode()
                                                            #tx_hash = hashlib.sha256(tx_string).hexdigest()
                                                            if(execute):
                                                                transactionComplete = False
                                                                try:    
                                                                    transactionComplete = BLOCKCHAIN_OBJECT.new_transaction(getOwnWalletFunc, newTx.getOutputAddress(), newTx.getOutputAmount(), newTx.getTransactionID(), newTx.getTimestamp(), newTx.getHash(), newTx.getPublic().to_string().hex(), newTx.getSignedData().hex(), str(newTx.getMetaData()))
                                                                except:
                                                                    transactionComplete = BLOCKCHAIN_OBJECT.new_transaction(getOwnWalletFunc, newTx.getOutputAddress(), newTx.getOutputAmount(), newTx.getTransactionID(), newTx.getTimestamp(), newTx.getHash(), newTx.getPublic().to_string().hex(), newTx.getSignedData(), str(newTx.getMetaData()))

                                                                if(transactionComplete):
                                                                    addTxToList(newTx)
                                                                    '''
                                                                    newBlock = BLOCKCHAIN_OBJECT.goNewBlock()

                                                                    if(newBlock):

                                                                        #print("Working 6")

                                                                        validatorLogger.logMessage("[BLOCKCHAIN] Block complete. Adding block to the blockchain", 'regular')

                                                                        BLOCKCHAIN_OBJECT.new_block(VALIDATOR_PEERS) # Creates new block if block meets all requirements\\


                                                                        #verifyBlock(blockchain.last_block_blockchain(), db)
                                                                    '''
                                                                    validatorLogger.logMessage("[Share Accepted] Share validated", 'success')
                                                        else:
                                                            validatorLogger.logMessage("[Share Rejected] User attempting to send coins to themself.", 'info-yellow')
                                                else:
                                                    validatorLogger.logMessage("[Share Rejected] User balance is too low to make transaction", 'info-yellow')
                                            else:
                                                # IS a duplicate transaction
                                                validatorLogger.logMessage("[Share Rejected] Transaction is duplicate", 'info-yellow')
                                        else:
                                            validatorLogger.logMessage("[Share Rejected] Fraud transaction detected", 'info-yellow')
                                    else:
                                        validatorLogger.logMessage("[Share Rejected] Wallet address does not match public key", 'info-yellow')
                        else:
                            validatorLogger.logMessage("[Share Rejected] Duplicate transaction recieved", 'info-yellow')

                except Exception as e:
                    validatorLogger.logMessage("[FATAL ERROR] Error occured with recieving data. " + str(e), 'error')
                    print(print(traceback.format_exc()))
                    #logging.log('message')

        except Exception as e:
            validatorLogger.logMessage("[FATAL ERROR] Validator error occured. " + str(e) + " Restart node.", 'error')

    def validatorRewardService():
        global txRecv
        global NETWORK
        global MINER_ID
        global NODE_PORT
        global NODE_IP
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
                    data = {'walletAddress': walletAddress, 'transactions': txRecv, 'minerID': MINER_ID, 'network': NETWORK, 'ip': NODE_IP, 'port': NODE_PORT}
                    managers = Connections().getManagerNodes()
                    validatorLogger.logMessage("[VALIDATOR CORE] Sending request for validator reward", 'info')
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
        validatorLogger.logMessage('[VALIDATOR CORE] Started spam protection service', 'info')
        while True:
            for i in range(SPAM_MANAGEMENT_SECONDS_LEFT, -1, - 1):
                time.sleep(1)
                SPAM_MANAGEMENT_SECONDS_LEFT_DOCUMENT = SPAM_MANAGEMENT_SECONDS_LEFT_DOCUMENT - 1
                #print(i)
            walletTxFreq = {} # Resets wallet spam threshold periodically
            SPAM_MANAGEMENT_SECONDS_LEFT = 86400
            SPAM_MANAGEMENT_SECONDS_LEFT_DOCUMENT = SPAM_MANAGEMENT_SECONDS_LEFT

    def getpeers():
        global VALIDATOR_PEERS
        while True:
            time.sleep(10) # Executes every 10 seconds
            validatorLogger.logMessage("[Peer Discovery Service] Getting list of peers", 'info')
            nodesData = Connections().getValidatorNodesWallet(NETWORK)
            #print(nodesData)
            if(nodesData != None):
                nodesFiltered = [] # Takes out own node from the list so doesn't double propagate
                for node in nodesData:
                    if(node['ip'] != NODE_IP and node['port'] != NODE_PORT):
                        nodesFiltered.append(node)
                VALIDATOR_PEERS = nodesFiltered
    
    async def syncBlockchain(syncUtil, syncNodeIP, syncNodePort, fullNodesList):
        global MINER_ID
        syncComplete = await syncUtil.chainInitSync(syncNodeIP, syncNodePort, fullNodesList, MINER_ID)
        #invoicePoolSync = await syncUtil.invoicePoolSync(fullNodesList)

        return syncComplete

    async def syncThread():
        global SPAM_MANAGEMENT_SECONDS_LEFT
        global BLOCKCHAIN_SYNC_COMPLETE
        global NETWORK
        global MINER_ID
        global TCP_PORT
    # Syncs the blockchain
        syncUtil = BlockchainSyncUtil.BlockchainSyncUtil()
        nodesDataTemp = syncUtil.getNodes(NETWORK)
        #print(nodesDataTemp)
        nodesDataList = []
        print(nodesDataTemp)

        if(nodesDataTemp['status'] == 'success'):
            # Filters out offline nodes
            for node in nodesDataTemp['data']:
                if(node['status'] == 'online'):
                    nodesDataList.append(node)
            nodesData = nodesDataTemp
            nodesData['data'] = nodesDataList
            #print(nodesData)
            currentTransactions = None
            while True:
                # IF getNodes is None
                if(nodesData == None):
                    execute = False
                    validatorLogger.logMessage('Error with connecting to network node. Restart validator and try again later.', 'regular')
                    break
                syncNodeIP, syncNodePort, nodeDataJSON = syncUtil.getRandomNode(MINER_ID, nodesData)

                if(syncNodeIP == True and syncNodePort == True and nodeDataJSON == True): # This is the first online node
                    validatorLogger.logMessage('[ONLINE] Detected as first online node', 'regular', False)
                    print("[ONLINE " + colored("⦾", 'green') + " ] Detected as first online node")
                    BLOCKCHAIN_SYNC_COMPLETE = True
                    break

                elif(syncNodeIP != None and syncNodePort != None and nodeDataJSON != None): # Is 
                    syncComplete = await syncBlockchain(syncUtil, syncNodeIP, syncNodePort, nodesData)# Blockchain is attempted to be synced
                    if(syncComplete): # If blockchain is synced
                        seconds, txFreqRecv = syncUtil.syncSpamManagementClock(syncNodeIP, syncNodePort)
                        if(seconds != None and txFreqRecv != None):
                            SPAM_MANAGEMENT_SECONDS_LEFT = seconds
                            walletTxFreq = txFreqRecv
                        BLOCKCHAIN_SYNC_COMPLETE = True 
                        #currentTransactions = currentTx
                        break
                    else: # Sync failed
                        # Remove this node from list
                        nodesData['data'].remove(nodeDataJSON)
                        pass
                else: # Blockchain could not be synced
                    #nodesData
                    validatorLogger.logMessage('An error has occured with syncing the blockchain', 'regular')
                    BLOCKCHAIN_SYNC_COMPLETE = False
            # Syncs with the blockchain
            #while BLOCKCHAIN_SYNC_COMPLETE != True:
            if(BLOCKCHAIN_SYNC_COMPLETE):
                print("Verifing blockchain integrity...")
                blockchainValid = BlockchainMongo().verifyBlockchainIntegrity()
                print("Done")
                if(blockchainValid):
                    # Start internal clock service
                    validatorLogger.logMessage('Starting internal node clock service...', 'regular')
                    clockUpdateService = threading.Thread(target=internalClockService)
                    clockUpdateService.start()
                    time.sleep(1)

                    # Save block service
                    validatorLogger.logMessage('Starting save block service...', 'regular')
                    saveBlockServiceDameon = threading.Thread(target=saveBlockService)
                    saveBlockServiceDameon.start()
                    
                    # Starts the main threads
                    t1 = threading.Thread(target=validatorServer, args=(('0.0.0.0', TCP_PORT), ))
                    grok = threading.Thread(target=runGrok)
                    # Starts spam protection service
                    spamProtection = threading.Thread(target=spamManagement)
                    validatorRewardServ = threading.Thread(target=validatorRewardService)
                    peerDiscoveryService = threading.Thread(target=getpeers)

                    # Starts the threads
                    try:
                        grok.start()
                        t1.start()
                        spamProtection.start()
                        #validatorRewardServ.start()
                        time.sleep(2)
                        validatorLogger.logMessage("Starting peer discovery service...", 'info')
                        peerDiscoveryService.start()
                    except Exception as err:
                        validatorLogger.logMessage("Node err has occured: " + str(err), 'regular')
                
                else:
                    validatorLogger.logMessage("[FATAL ERROR] Blockchain is not valid. Please restart this node and download the latest blockchain.", 'error')
                    x = input("(Press any key to exit)>>")
            else:
                x = input("(Press any key to exit)>>")
        else: 
            validatorLogger.logMessage("[FATAL ERROR] Error with fetching validators from network node", 'error')
            x = input("(Press any key to exit)>>")

    if __name__ == "__main__":
        # Checks if miner wallet exists
        if(path.exists('key.pem')):
            # Loads wallet details
            myPrivateSigning, myVerifyingKey = SignaturesECDSA().loadKey()
            walletAddress, wif = SignaturesECDSA().make_address(myVerifyingKey.to_string())
            VALIDATOR_PRIVATE, VALIDATOR_PUBLIC_KEY = myPrivateSigning, myVerifyingKey
            VALIDATOR_WALLET_ADDRESS = walletAddress
            # Loads node configuration
            loadComplete = loadConfiguration()
            if(NETWORK == "testnet"):
                validatorLogger.logMessage("[VALIDATOR CORE][WARNING] Validator node is running in testnet mode. If you want to run in mainnet, change the 'network' option to 'mainnet' in the config.json", 'warning')
            #time.sleep(3)
            if(loadComplete):
                # Creates the /blockchain dir if not exist
                '''
                current_directory = os.getcwd()

                final_directory = os.path.join(current_directory, r'Blockchain')
                if not os.path.exists(final_directory):
                    validatorLogger.logMessage('Creating blockchain directory', 'regular')
                    os.makedirs(final_directory)
                '''
                validatorLogger.logMessage('Starting validator node', 'regular')
                validatorLogger.logMessage("[INTERNAL SERVER] Running connection test", 'info')
                # Runs connection test to the network
                allTestsPassed = Connections().connectionTest()
                #print(allTestsPassed)
                if(allTestsPassed):
                    #print("All tests passed")
                    try:
                        asyncio.run(syncThread())
                    except Exception as e:
                        print("Error with blockchain sync thread: " + str(e))
                        print(traceback.format_exc())
                else:
                    validatorLogger.logMessage("Connection tests failed. Restart node or try again later", 'error')
                    x = input("(Press any key to exit)>>")
            else: # Error has occured
                x = input("(Press any key to exit)>>")
        else:
            validatorLogger.logMessage("Validator wallet does not exist. Run 'python GenerateWallet.py' and run the validator node again.", 'error')
            x = input("(Press any key to exit)>>")

except Exception as e:
    print("Error with validator: " + str(e))
    print(traceback.format_exc())
    x = input("(Press any key to exit)>>")