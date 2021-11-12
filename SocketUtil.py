# Imports
import time
import traceback
from connections import Connections
from SignaturesECDSA import SignaturesECDSA
from Signatures import Signatures
import socket
import pickle
from colorama import init 
from termcolor import colored 
import requests


init()
# Global Variables
TCP_PORT = 5005
# Functions

class SocketUtil:

    def __init__(self):
        pass

    def verifyTransactionRaw(self, tx, public):

        try:

            verified = False

            originalData = []

            originalData.append(tx['recipient'])
            originalData.append(tx['amount'])
            originalData.append(tx['timestamp'])
            originalData.append(tx['publicKey'])
            originalData.append(tx['transactionID'])

            #print(bytes(str(originalData), 'utf-8').hex())

            #print(originalData)

            verified = SignaturesECDSA().verify(bytes(str(originalData), 'utf-8'), bytes.fromhex(tx['signedMessage']), public)
            return verified

        
        except Exception as e: # On error
            print(" Error occured verifyTransactionRaw - SocketUtil.py: " + str(e))
            print(traceback.format_exc())
            return False

    def verifyTransaction(self, transaction, public):

        try:

            #print(transaction.data)

            #print(transaction.signedData)

            #message, sig, verifyingKey

            #print(transaction)
            #print(public)

            verified = False

            #print(transaction.getTxType())

            if(transaction.getTxType() == 'mobile'):
                #print("mobile transaction")
                verifed = SignaturesECDSA().verify(transaction.getMobileSignedData(), bytes.fromhex(transaction.getSignedData()), public)

            else:
                #print("regular transaction")
                #print(bytes(str(transaction.getData()), 'utf-8').hex())
                #print(transaction.getData())

                verifed = SignaturesECDSA().verify(bytes(str(transaction.getData()), 'utf-8'), transaction.getSignedData(), public)

            #print(verifed)

            #print(transaction.getOutputAmount())

            if verifed == True: #  Checks if transaction is valid
                if transaction.getOutputAmount() > 0: # Checks if transaction amount is greater than zero
                    return True
                else: # If transaction value is less than zero
                    print(colored("[Share Rejected] Transaction value is less than zero", 'yellow'))
                    return False
            
            else: # If transaction is not valid
                return False
        
        except Exception as e: # On error
            print(" Error occured verifyTransaction - SocketUtil.py: " + str(e))
            print(traceback.format_exc())
            return False

    def newServerConnection(ip_addr, port=TCP_PORT):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((ip_addr, port))
        s.listen(9096)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 10485760)  
        return s
    
    def sendObj(ip_addr, inObj, port, timeout=None):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        #print("TIMEOUT: " + str(timeout))
        if(timeout != None):
            s.setblocking(0)
            s.settimeout(timeout)

        s.connect((ip_addr, port))
        data = pickle.dumps(inObj)
        s.send(data)
        s.close()



    
    def updateMinerIp(ip, validatorID, net, publicKey, walletAddr, privateKey):
        
        # Orignial Data
        # - ip + port + id + network

        ip = ip[6:]

        colon = ip.find(":")

        port = ip[colon + 1:]
        ip = ip[:colon]

        data = str(validatorID) + str(ip) + str(port) + str(net) + str(walletAddr) + str(publicKey)

        signature = ''

        try:
            signature = privateKey.sign(bytes(str(data), 'utf-8')).hex()
      
        except Exception as e:
            print("Error with signing signature: " + str(e))
        
        networkNodes = Connections().getNetworkNodes()

        rtnStatement = None

        for node in networkNodes:
            try:
                r = requests.get(node + '/validator/update?ip=' + str(ip) + "&port=" + str(port) + "&id=" + str(validatorID) + "&network=" + str(net) + "&publicKey=" + str(publicKey) + "&walletAddr=" + str(walletAddr) + "&signature=" + str(signature))
                #print("Updated miner ip: " + str(r.json()))

                data = r.json()

                if(data['status'] == 'failed'):
                    print(colored("Network node update request failed: " + str(data['message']), "yellow"))
                    return None, None

                else:
                    rtnStatement =  ip, int(port)
                    break

            except Exception as e:
                print("[FATAL ERROR] Network node is offline: " + str(e))
                rtnStatement = None, None

            #doc = db.collection(u'Miner Nodes').document(minerID)

            #doc.set({
                #"ip": ip,
                #"port": int(port)
            #})
            
        
        return rtnStatement
    

    def updateMinerIpTCP_MODE(ip, port, minerID, net):

        networkNodes = Connections().getNetworkNodes()

        rtnStatement = False

        for node in networkNodes:
            try:
                r = requests.get(node + '/validator/update?ip=' + str(ip) + "&port=" + str(port) + "&id=" + str(minerID) + "&network=" + str(net))
                #print("Updated miner ip: " + str(r.json()))
                rtnStatement = True
                break

            except Exception as e:
                print("[FATAL ERROR] Network node is offline: " + str(e))
                rtnStatement = False

            #doc = db.collection(u'Miner Nodes').document(minerID)

            #doc.set({
                #"ip": ip,
                #"port": int(port)
            #})
        
        return rtnStatement


